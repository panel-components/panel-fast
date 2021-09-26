import param

from panel.io.server import init_doc, state
from panel.layout import ListLike
from panel.reactive import ReactiveHTML

CSS_FILES = [
    "static/extensions/panel/bundled/fastbasetemplate/fast_bokeh.css",
    "static/extensions/panel/bundled/fastbasetemplate/fast_bokeh_slickgrid.css",
    "static/extensions/panel/bundled/fastbasetemplate/fast_panel.css",
    "static/extensions/panel/bundled/fastbasetemplate/fast_panel_dataframe.css",
    "static/extensions/panel/bundled/fastbasetemplate/fast_panel_widgets.css",
    "static/extensions/panel/bundled/fastbasetemplate/fast_panel_markdown.css",
    "static/extensions/panel/bundled/fastbasetemplate/fast_awesome.css",
    "static/extensions/panel/bundled/fastbasetemplate/fast_root.css",
    "static/extensions/panel/bundled/fastlisttemplate/fast_list_template.css",
]


class FastDesignProvider(ListLike, ReactiveHTML):
    background_color = param.Color("#181818", doc="""The background Color""")
    neutral_color = param.Color("#767676")
    accent_color = param.Color("#DA1A5F")
    corner_radius = param.Integer(default=4, bounds=(0, 25))

    body_provider = param.Boolean(False, constant=True, doc="""
        Set to True if this is the outer FastDesignProvider containing all of the other components
    """)

    _template = """\
{% if body_provider %}
<style>
.bk-root .bk-input {
    width: calc(100% - 24px);
}
</style>
{% endif %}
<fast-design-system-provider id="fdsp"
{% if body_provider %}class="body-provider"{% endif %}
use-defaults>
{% for obj in objects %}
<div id="provider-item" class="provider-item" style="margin-top:20px">${obj}</div>
{% endfor %}
</fast-design-system-provider>
"""

    _scripts = {
        "render": """
state.fdspId="#fdsp-" + data.id.toString()
providerElement=document.querySelector(state.fdspId)

if (data.body_provider === true){
    bodyElement = document.getElementsByTagName("body")[0]
    bodyElement.style.paddingRight = "10px";
    bodyElement.style.background = data.background_color
    providerElement.style.minHeight="100vh"
    providerElement.style.minWidth="calc(100vw - 10px)"
}
window.fastDesignProvider.configure( data.background_color, data.neutral_color, data.accent_color, state.fdspId)
providerElement.cornerRadius=data.corner_radius;
setTimeout(function(){window.dispatchEvent(new Event('resize'))}, 25);
""",
        "background_color": """
if (data.body_provider === true){
    bodyElement = document.getElementsByTagName("body")[0]
    bodyElement.style.padding = "10px";
    bodyElement.style.background = data.background_color
    providerElement.style.minHeight="100vh"
    providerElement.style.minWidth="calc(100vw - 10px)"
}
window.fastDesignProvider.configure( data.background_color, data.neutral_color, data.accent_color, state.fdspId);""",
        "accent_color": """window.fastDesignProvider.configure( data.background_color, data.neutral_color, data.accent_color, state.fdspId);""",
        "neutral_color": """window.fastDesignProvider.configure( data.background_color, data.neutral_color, data.accent_color, state.fdspId);""",
        "corner_radius": """document.querySelector(state.fdspId).cornerRadius= data.corner_radius ;""",
    }

    __javascript_modules__ = [
        "https://unpkg.com/@microsoft/fast-colors@5.1.0",
        "https://unpkg.com/@microsoft/fast-components@1.13.0",
        "https://cdn.jsdelivr.net/gh/MarcSkovMadsen/awesome-panel-assets/js/panel_fast@0.0.1.js",
    ]

    __css__ = CSS_FILES

    @param.depends("background", watch=True)
    def _update_background_color(self):
        self.background_color=self.background

class FastComponent(ReactiveHTML):

    sizing_mode = param.ObjectSelector(default='stretch_width', objects=[
        'fixed', 'stretch_width', 'stretch_height', 'stretch_both',
        'scale_width', 'scale_height', 'scale_both', None])

    __abstract = True

    def get_root(self, doc=None, comm=None, preprocess=True):
        doc = init_doc(doc)
        root_obj = FastDesignProvider()
        root_obj.append(self)
        root = root_obj.get_root(doc, comm, False)
        if preprocess:
            root_obj._preprocess(root)
        ref = root.ref['id']
        state._views[ref] = (self, root, doc, comm)
        return root
