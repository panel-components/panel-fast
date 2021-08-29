import param

from panel.widgets.select import SelectBase

from .base import FastComponent


class FastNumberInput(FastComponent):

    appearance = param.Selector(default='outline', objects=['outline', 'filled'])

    autofocus = param.Boolean(default=False)

    placeholder = param.String(default='Type here')

    step = param.Number(default=0)

    start = param.Number(default=0)

    end = param.Number(default=1)

    value = param.Number(default=0)

    _child_config = {'name': 'template'}

    _template= '<fast-number-field id="fast-number" autofocus="${autofocus}" placeholder="${placeholder}" step="${step}" value="${value}" min="${start}" max="${end}" appearance="${appearance}"></fast-number-field>'

    _dom_events = {'fast-number': ['change']}


class FastSlider(FastComponent):

    height = param.Integer(default=50)

    step = param.Number(default=0.1)

    start = param.Number(default=0)

    end = param.Number(default=1)

    value = param.Number(default=0)

    _child_config = {'name': 'template'}

    _template = '<fast-slider id="fast-slider" value="${value}" min="${start}" max="${end}" step="${step}"></fast-slider>'


class FastSelect(FastComponent, SelectBase):

    options = param.ClassSelector(default=[], class_=(dict, list))

    value = param.Parameter()

    _template = """
    <fast-select value="${value}" id="fast-select">
    {% for option in options %}
      <fast-option value="{{ option }}">${option}</fast-option>
    {% endfor %}
    </fast-select>
    """

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        if 'value' in msg:
            msg['value'] = self._items[msg['value']]
        return msg


class FastButton(FastComponent):

    clicks = param.Integer(default=0, bounds=(0, None))

    value = param.Event()

    _child_config = {'name': 'template'}

    _template = '<fast-button onclick="${_on_click}" appearance="outline" id="fast-button">${name}</fast-button>'

    def _on_click(self, event):
        self.clicks += 1
        self.param.trigger('value')


class FastCheckbox(FastComponent):

    value = param.Boolean(default=True)

    _child_config = {'name': 'template'}

    _template = '<fast-checkbox value="${value}">${name}</fast-checkbox>'


class FastRadioGroup(FastComponent, SelectBase):

    options = param.ClassSelector(default=[], class_=(dict, list))

    value = param.Parameter()

    _child_config = {'options': 'literal'}

    _template = """
    <fast-radio-group value="${value}" id="fast-radio-group">
      <label style="color: var(--neutral-foreground-rest);" slot="label" slot="label">${title}</label>
      {% for option in options %}
      <fast-radio id="fast-radio-{{ loop.index0 }}">${options[{{ loop.index0 }}]}</fast-radio>
      {% endfor %}
      </fast-radio-group>
    """

    def _on_change(self, event):
        self.value = self._items[event.data['value']]

    def _process_children(self, doc, root, model, comm, children):
        children['fast-options'] = self.labels
        return children


class FastToggle(FastComponent):

    value = param.Boolean(default=False)

    _template = '<fast-switch checked="${value}">${name}</fast-switch>'


class FastTextArea(FastComponent):

    value = param.String()

    _template = '<fast-text-area value="${value}"></fast-text-area>'


class FastTextInput(FastComponent):

    placeholder = param.String()

    value = param.String()

    _template = '<fast-text-field placeholder="${placeholder}" value="${value}"></fast-text-field>'


class FastProgress(FastComponent):

    _template = '<fast-progress></fast-progress>'


class FastProgressRing(FastComponent):

    _template = '<fast-progress-ring></fast-progress-ring>'
