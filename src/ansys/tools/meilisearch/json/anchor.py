class ElementAnchor:
    def __init__(self):
        pass

    def get_anchor_string(element):
        """Return the anchor string from the given element."""
        return element.get("name") or element.get("id")

    def get_anchor(cls, element):
        """Return the first possible anchor for the given element."""
        if isinstance(element, str):
            return None

        # Check the name or id on the element
        anchor = cls.get_anchor_string(element)

        if anchor:
            return anchor

        # Check on children
        children = element.cssselect("[name],[id]")
        if children:
            return cls.get_anchor_string(children[-1])

        # Check previous siblings
        for sibling in element.iterprevious():
            anchor = cls.get_anchor_string(sibling)
            if anchor:
                return anchor

        # Check parent
        parent = element.getparent()
        if parent is not None:
            anchor = cls.get_anchor_string(parent)
            if anchor:
                return anchor

        # No anchor found
        return None
