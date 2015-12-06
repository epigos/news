import pyquery


def html_values(html, selector, **format_attr):
    """Get html values by providing a html and selector/selectors.

    Get the text value with single selector:

        >>> html = '<div><span>toto</span><span>tata</span></div>'
        >>> selector = 'span'
        >>> print(html_values(html, selector))
        ['toto', 'tata']

    Get the text value with multiple selector (Note: results are returned from the first matched
    selector and any further selector is ignored). If attribute is provided in a tuple, then data
    from attr is extracted. Example:

        >>> html = '<div><span data="somo">toto</span><span data="sama">tata</span></div>'
        >>> selector = ['img', ('span[data]', 'data'), 'span']
        >>> print(html_values(html, selector))
        ['somo', 'sama']

    Multiple attributes are also supported. First matched attribute will return a result. Example:

        >>> html = '<div><span data="first" href="second">toto</span></div>'
        >>> selector = ['img', ('[data]', ['src', 'data', 'href'])]
        >>> print(html_values(html, selector))
        ['first']

    Also filter tags can be specified in selector for which values are added as an argument.
    Example:

        >>> html = '<span class="item1">first item</span><span class="item2">second item</span>'
        >>> selector = ['.item{product_id}']
        >>> print(html_values(html, selector, product_id=1))
        ['first item']
    """
    # if string is provided as selector, then convert it to list
    selectors = selector if isinstance(selector, list) else [selector]
    for selector in selectors:
        selector = selector
        attributes = None
        if isinstance(selector, tuple):
            selector, attributes = selector

        selector = selector.format(**format_attr)

        values = []
        pq = pyquery.PyQuery(html)(selector)

        for tag in pq.items():
            if attributes is not None:
                attributes = [attributes] if isinstance(attributes, str) else attributes
                for attribute in attributes:
                    if tag.attr(attribute):
                        values.append(tag.attr(attribute))
                        break
            else:
                values.append(tag.text())

        if values:
            return values
    return []


def html_value(html, selectors, **format_attr):
    """Get html values by providing a html and selector/selectors.

    Works exactly the same as "html_values", but returns only one
    value instead list of values:

        >>> html = '<div><span data="first" href="second">toto</span></div>'
        >>> selector = ['img', ('[data]', ['src', 'data', 'href'])]
        >>> print(html_value(html, selector))
        first
    """
    values = html_values(html, selectors, **format_attr)
    return values[0] if values else None
