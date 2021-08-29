from collections import defaultdict

import param

from panel.io.server import init_doc, state
from panel.reactive import ReactiveHTML


class FastDesignProvider(ListLike, ReactiveHTML):
        
    _template = '<fast-design-system-provider id="fdsp" use-defaults>${objects}</fast-design-system-provider>'


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
