"""
Default Strategy
"""

import hashlib
import json
import re
import sys

from lxml.etree import XPath

from .anchor import Anchor
from .converter import Hierarchy


class DefaultStrategy:
    """
    DefaultStrategy
    """

    dom = None

    def __init__(self, config):
        self.config = config
        self.levels = ["lvl0", "lvl1", "lvl2", "lvl3", "lvl4", "lvl5", "lvl6"]
        self.global_content = {}
        self.page_rank = {}

    def select(self, path):
        """Select an element in the current DOM using specified CSS selector"""
        return XPath(path)(self.dom) if len(path) > 0 else []

    def _update_hierarchy_with_global_content(self, hierarchy, current_level_int):
        for index in range(0, current_level_int + 1):
            if f"lvl{index}" in self.global_content:
                hierarchy[f"lvl{index}"] = self.global_content[f"lvl{index}"]

        return hierarchy

    def _update_record_with_global_content(self, record, levels):
        for level in levels:
            if "lvl" not in level and level not in ["content", "text"]:
                record[level] = self.global_content[level]

        return record

    def _get_used_levels(self, selectors):
        levels = list(self.levels)
        used_levels = []
        for level in levels:
            if level not in selectors:
                break
            used_levels.append(level)

            if "content" in selectors:
                used_levels.append("content")

            return used_levels

    def get_selectors_set_key(self, url):
        selectors_key = "default"

        if url is not None:
            for start_url in self.config.start_urls:
                if re.search(start_url["compiled_url"], url) is not None:
                    selectors_key = start_url["selectors_key"]
                    break

        return selectors_key

    def get_selectors_set(self, url):
        selectors_key = self.get_selectors_set_key(url)

        if selectors_key not in self.config.selectors:
            return self.config.selectors["default"]

        return self.config.selectors[selectors_key]

    def to_json(self, my_json):
        try:
            jsonized = json.loads(my_json)
        except ValueError:
            return None
        return jsonized

    def get_records_from_dom(self, current_page_url=None):
        if self.dom is None:
            sys.exit("DefaultStrategy.dom is not defined")

        # Reset it to be able to have a clean instance when testing
        self.global_content = {}

        selectors = self.get_selectors_set(current_page_url)
        levels = self._get_used_levels(selectors)

        # We get a big selector that matches all relevant nodes, in order
        # But we also keep a list of all matches for each individual level
        nodes_per_level = self._get_nodes_per_level(selectors, levels)
        nodes = self._get_all_matching_nodes(levels, selectors)
        self._get_nodes_per_global_level(selectors, levels)

        # We keep the current hierarchy and anchor state between loops
        previous_hierarchy = self._generate_empty_hierarchy()
        anchors = self._generate_empty_hierarchy()

        records = []

        for position, node in enumerate(nodes):
            current_level = self._get_level_of_node(node, nodes_per_level, levels)

            # We copy the previous hierarchy, We override the current level,
            # And set all levels after it to None
            hierarchy = previous_hierarchy.copy()

            # Update the hierarchy for each new header
            current_level_int = levels.index(current_level)

            if current_level != "content":
                hierarchy[current_level] = self._get_text_content_for_level(
                    node, current_level, selectors
                )
                anchors[current_level] = Anchor.get_anchor(node)

                for index in range(current_level_int + 1, 7):
                    hierarchy[f"lvl{index}"] = None
                    anchors[f"lvl{index}"] = None
                previous_hierarchy = hierarchy

                if self.config.only_content_level:
                    continue

            if current_level_int < self.get_min_indexed_level_for_url(current_page_url):
                continue

            hierarchy = self._update_hierarchy_with_global_content(hierarchy, current_level_int)

            # We only save content for the 'text' matches
            content = (
                None
                if current_level != "content"
                else self.get_text(node, self.get_strip_chars(current_level, selectors))
            )

            if (content is None or content == "") and current_level == "content":
                continue

            hierarchy, content = self._handle_default_values(
                hierarchy, content, selectors, self.levels
            )

            # noinspection PyDictCreation
            record = {
                "anchor": self._get_closest_anchor(anchors),
                "content": content,
                "hierarchy": hierarchy,
                "hierarchy_radio": Hierarchy.get_hierarchy_radio(hierarchy, current_level, levels),
                "type": current_level,
                "weight": {
                    "level": self.get_level_weight(current_level),
                    "position": position,
                },
                "url": current_page_url,
                "url_without_variables": current_page_url,
            }

            record["hierarchy_camel"] = (record["hierarchy"],)
            record["hierarchy_radio_camel"] = record["hierarchy_radio"]
            record["content_camel"] = record["content"]

            self._update_record_with_global_content(record, selectors)

            # get meta data
            for meta_node in self.select("//meta"):
                name = meta_node.get("name")
                content = meta_node.get("content")
                if name and name.startswith("docs-scraper:") and content:
                    name = name.replace("docs-scraper:", "")
                    jsonized = self.to_json(content)
                    if jsonized:
                        record[name] = jsonized
                    else:
                        record[name] = content

                    if name == "version":
                        record[name] = str(record[name])

            if current_page_url is not None:
                # Add variables to the record

                record["url_without_anchor"] = record["url"]
                record["url"] = self._get_url_with_anchor(record["url"], record["anchor"])
                record["url_without_variables"] = self._get_url_with_anchor(
                    record["url_without_variables"], record["anchor"]
                )
                record["no_variables"] = record["url"] == record["url_without_variables"]

            # Define our own ObjectID to enable proper analytics
            hierarchy_to_hash = {lvl: x for lvl, x in hierarchy.items() if x is not None}
            raw_hash = hashlib.sha1(
                json.dumps(
                    {
                        "hierarchy_to_hash": hierarchy_to_hash,
                        "url": record["url"],
                        "position": position,
                    },
                    sort_keys=True,
                ).encode("utf-8")
            )
            digest_hash = raw_hash.hexdigest()
            record["objectID"] = digest_hash
            records.append(record)

        return records

    def _get_text_content_for_level(self, node, current_level, selectors):
        if "attributes" in selectors[current_level]:
            attributes = {}
            for attribute_name in list(selectors[current_level]["attributes"].keys()):
                matching_nodes = node.xpath(
                    selectors[current_level]["attributes"][attribute_name]["selector"]
                )
                attributes[attribute_name] = self.get_text_from_nodes(
                    matching_nodes,
                    self.get_strip_chars(attribute_name, selectors[current_level]["attributes"]),
                )
            return attributes

        if current_level in self.global_content:
            return self.global_content[current_level]

        return self.get_text(node, self.get_strip_chars(current_level, selectors))

    @staticmethod
    def _get_closest_anchor(anchors):
        # Getting the element anchor as the closest one
        for index in list(range(6, -1, -1)):
            potential_anchor = anchors[f"lvl{index}"]
            if potential_anchor is None:
                continue
            return potential_anchor

        return None

    @staticmethod
    def _get_level_of_node(node, nodes_per_level, levels):
        for level in levels:
            if level in nodes_per_level:  # if it's global we won't have it
                if node in nodes_per_level[level]:
                    return level

        return None

    @staticmethod
    def _handle_default_values(hierarchy, content, selectors, levels):
        # Handle default values
        for level in selectors:
            if level in levels:
                if hierarchy[level] is None and selectors[level]["default_value"] is not None:
                    hierarchy[level] = selectors[level]["default_value"]
            elif level == "content":
                if content is None and selectors[level]["default_value"] is not None:
                    content = selectors["content"]["default_value"]

        return hierarchy, content

    def _get_nodes_per_global_level(self, selectors, levels):
        for level in list(selectors.keys()):
            level_selector = selectors[level]
            if level not in levels or level_selector["global"]:
                matching_dom_nodes = self.select(level_selector["selector"])
                self.global_content[level] = self.get_text_from_nodes(
                    matching_dom_nodes, self.get_strip_chars(level, selectors)
                )

                if (
                    self.global_content[level] is None
                    and level_selector["default_value"] is not None
                ):
                    self.global_content[level] = level_selector["default_value"]

    def _get_nodes_per_level(self, selectors, levels):
        nodes_per_level = {}

        for level in levels:
            level_selector = selectors[level]
            matching_dom_nodes = self.select(level_selector["selector"])

            if not level_selector["global"]:
                nodes_per_level[level] = matching_dom_nodes

        return nodes_per_level

    def _get_all_matching_nodes(self, levels, selectors):
        return self.select(" | ".join(self._get_selector_all(levels, selectors)))

    @staticmethod
    def _get_selector_all(levels, selectors):
        selector_all = []
        for level in levels:
            level_selector = selectors[level]

            if len(level_selector["selector"]) > 0 and not level_selector["global"]:
                selector_all.append(level_selector["selector"])

        return selector_all

    def _get_url_with_anchor(self, current_page_url, anchor):
        if (not self.config.js_render or not self.config.use_anchors) and anchor is not None:
            return current_page_url + "#" + anchor

        return current_page_url
