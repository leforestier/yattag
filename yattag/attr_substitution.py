
__all__ = ['add_svg_attributes', 'reset_attr_substitutions']

DEFAULT_ATTR_SUBSTITUTION_MAP = {
    "klass": "class",
}

SVG_ATTR_SUBSTITUTIONS = {
    "font_face": "font-face",
    "font_face_format": "font-face-format",
    "font_face_name": "font-face-name",
    "font_face_src": "font-face-src",
    "font_face_uri": "font-face-uri",
    "missing_glyph": "missing-glyph",
    "glyph_name": "glyph-name",
    "cap_height": "cap-height",
    "horiz_adv_x": "horiz-adv-x",
    "horiz_adv_y": "horiz-adv-y",
    "horiz_origin_x": "horiz-origin-x",
    "horiz_origin_y": "horiz-origin-y",
    "overline_position": "overline-position",
    "overline_thickness": "overline-thickness",
    "panose_1": "panose-1",
    "rendering_intent": "rendering-intent",
    "strikethrough_position": "strikethrough-position",
    "strikethrough_thickness": "strikethrough-thickness",
    "underline_position": "underline-position",
    "underline_thickness": "underline-thickness",
    "unicode_range": "unicode-range",
    "units_per_em": "units-per-em",
    "v_alphabetic": "v-alphabetic",
    "v_hanging": "v-hanging",
    "v_ideographic": "v-ideographic",
    "v_mathematical": "v-mathematical",
    "vert_adv_y": "vert-adv-y",
    "vert_adv_y": "vert-adv-y",
    "vert_origin_x": "vert-origin-x",
    "vert_origin_x": "vert-origin-x",
    "vert_origin_y": "vert-origin-y",
    "vert_origin_y": "vert-origin-y",
    "x_heght": "x-heght",
    "xlink_actuate": "xlink:actuate",
    "xlink_actuate": "xlink:actuate",
    "xlink_arcrole": "xlink:arcrole",
    "xlink_href": "xlink:href",
    "xlink_role": "xlink:role",
    "xlink_show": "xlink:show",
    "xlink_show": "xlink:show",
    "xlink_title": "xlink:title",
    "xlink_type": "xlink:type",
    "xml_base": "xml:base",
    "xml_lang": "xml:lang",
    "alignment_baseline": "alignment-baseline",
    "baseline_shift": "baseline-shift",
    "clip_path": "clip-path",
    "clip_rule": "clip-rule",
    "color_interpolation_filters": "color-interpolation-filters",
    "color_interpolation": "color-interpolation",
    "color_profile": "color-profile",
    "color_rendering": "color-rendering",
    "dominant_baseline": "dominant-baseline",
    "enable_background": "enable-background",
    "fill_opacity": "fill-opacity",
    "fill_rule": "fill-rule",
    "flood_color": "flood-color",
    "flood_opacity": "flood-opacity",
    "font_family": "font-family",
    "font_size_adjust": "font-size-adjust",
    "font_size": "font-size",
    "font_stretch": "font-stretch",
    "font_style": "font-style",
    "font_variant": "font-variant",
    "font_weight": "font-weight",
    "glyph_orientation_horizontal": "glyph-orientation-horizontal",
    "glyph_orientation_vertical": "glyph-orientation-vertical",
    "image_rendering": "image-rendering",
    "letter_spacing": "letter-spacing",
    "lighting_color": "lighting-color",
    "marker_end": "marker-end",
    "marker_mid": "marker-mid",
    "marker_start": "marker-start",
    "pointer_events": "pointer-events",
    "shape_rendering": "shape-rendering",
    "stop_color": "stop-color",
    "stop_opacity": "stop-opacity",
    "stroke_dasharray": "stroke-dasharray",
    "stroke_dashoffset": "stroke-dashoffset",
    "stroke_linecap": "stroke-linecap",
    "stroke_linejoin": "stroke-linejoin",
    "stroke_miterlimit": "stroke-miterlimit",
    "stroke_opacity": "stroke-opacity",
    "stroke_width": "stroke-width",
    "text_anchor": "text-anchor",
    "text_decoration": "text-decoration",
    "text_rendering": "text-rendering",
    "unicode_bidi": "unicode-bidi",
    "word_spacing": "word-spacing",
    "writing_mode": "writing-mode",
}


class AttrSubstitution(object):
    current_map = DEFAULT_ATTR_SUBSTITUTION_MAP.copy()

    @classmethod
    def translate(cls, attr_name):
        """ get fixed atribute from map or return unchanged if not found """
        return cls.current_map.get(attr_name, attr_name)


def add_svg_attributes():
    """ Call it anywhere in your script to enable a helper that allows for
    adding attributes natively containing minus caracter in name, as a keyword
    argument of tag and stag yattag methds. Underscores in known attributes will
    be replaced with minus'es.

    Regulary to produce e.g.::

        <font-face font-family="Sans" units-per-em="1000 />

    without the helper you need to type:

        doc.stag("font-face", ("font-family", "Sans"), ("units-per-em", 1000)

    after calling add_svg_attributes() it can also be::

        doc.stag("font-face", font_family = "Sans", units_per_em = 1000)

    (Note the underscores, that avoids python syntax errors)

    You can disable the helper anytime by calliing reset_attr_substitutions()
    """

    AttrSubstitution.current_map.update(SVG_ATTR_SUBSTITUTIONS)


def reset_attr_substitutions():
    """ Reset all modifications made to attribute substitution helper,
        e.g. if add_svg_attributes() has been invoked.
    """
    AttrSubstitution.current_map = DEFAULT_ATTR_SUBSTITUTION_MAP.copy()
