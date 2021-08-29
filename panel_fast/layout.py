import param

from panel.layout.base import ListLike, NamedListLike

from .base import FastComponent


class FastDivider(FastComponent):

    _template = '<fast-divider></fast-divider>'


class FastCard(FastComponent, ListLike):
    
    _template = '<fast-card id="fast-card">${objects}</fast-card>'
    
    def __init__(self, *objects, **params):
        super().__init__(objects=list(objects), **params)


class FastDialog(FastComponent, ListLike):
    
    hidden = param.Boolean(default=False)
    
    _template = """
    <fast-dialog id="fast-dialog" hidden=${hidden} style="z-index: 100; --dialog-width: 80%; --dialog-height: 80%">
      <fast-button id="close-button" onclick="${_close}" style="float: right">X</fast-button>
      ${objects}
    </fast-dialog>
    """
    
    def __init__(self, *objects, **params):
        super().__init__(objects=list(objects), **params)
        
    def _close(self, event):
        self.hidden = True


class FastTabs(FastComponent, NamedListLike):
    
    _template = """
    <fast-tabs id="fast-tabs">
    {% for obj_name in objects_names %}
      <fast-tab slot="tab" slot="tab">{{ obj_name }}</fast-tab>
    {% endfor %}
    {% for object in objects %}
      <fast-tab-panel id="fast-tab-panel" slot="tabpanel" slot="tabpanel">${object}</fast-tab-panel>
    {% endfor %}
    </fast-tabs>
    """
    
    @property
    def _child_names(self):
        return {'objects': self._names}

    def __init__(self, *objects, **params):
        NamedListLike.__init__(self, *objects, **params)
        FastComponent.__init__(self, objects=self.objects, **params)
