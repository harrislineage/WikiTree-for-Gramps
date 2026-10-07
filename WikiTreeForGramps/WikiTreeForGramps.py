"""WikiTree for Gramps add-on for Gramps 6.0.x.

Adds WikiTree profile integration to the Gramps Person Editor.
"""

import re
from urllib.parse import unquote, urlparse

from gi.repository import Gtk

from gramps.gen.lib import Attribute
from gramps.gui.display import display_url
from gramps.gui.editors.editperson import EditPerson


ATTRIBUTE_NAME = "WikiTree ID"
WIKITREE_BASE = "https://www.wikitree.com/wiki/"
ID_RE = re.compile(r"^[^/\\\s]+-\d+$")


_patched = False
_original_post_init = None
_original_save = None


def _normalize_wikitree_id(value):
    """Normalize a WikiTree ID or WikiTree profile URL."""
    value = (value or "").strip()

    if not value:
        return ""

    if "://" in value:
        parsed = urlparse(value)

        if parsed.netloc.lower() in {"wikitree.com", "www.wikitree.com"}:
            path = unquote(parsed.path).rstrip("/")

            if "/wiki/" in path:
                value = path.rsplit("/wiki/", 1)[1]
            else:
                value = path.rsplit("/", 1)[-1]

    return value.strip()


def _get_wikitree_id(person):
    """Return the WikiTree ID stored for a person."""
    for attr in person.get_attribute_list():
        if str(attr.get_type()) == ATTRIBUTE_NAME:
            return attr.get_value() or ""

    return ""


def _set_wikitree_id(person, value):
    """Create, update, or remove the WikiTree ID attribute."""
    value = _normalize_wikitree_id(value)

    matches = [
        attr
        for attr in person.get_attribute_list()
        if str(attr.get_type()) == ATTRIBUTE_NAME
    ]

    if value:
        if matches:
            matches[0].set_value(value)

            for extra in matches[1:]:
                person.remove_attribute(extra)
        else:
            attr = Attribute()
            attr.set_type(ATTRIBUTE_NAME)
            attr.set_value(value)
            person.add_attribute(attr)

    else:
        for attr in matches:
            person.remove_attribute(attr)


def _entry_changed(entry, button):
    """Enable the WikiTree button when the entered ID is valid."""
    value = _normalize_wikitree_id(entry.get_text())
    button.set_sensitive(bool(value and ID_RE.fullmatch(value)))


def _entry_focus_out(entry, _event):
    """Normalize pasted WikiTree URLs when leaving the field."""
    normalized = _normalize_wikitree_id(entry.get_text())

    if normalized != entry.get_text():
        entry.set_text(normalized)

    return False


def _open_wikitree(_button, editor):
    """Open the WikiTree profile in the default browser."""
    value = _normalize_wikitree_id(
        editor.wikitree_id_entry.get_text()
    )

    if ID_RE.fullmatch(value):
        display_url(WIKITREE_BASE + value, editor.uistate)


def _add_wikitree_field(editor):
    """Add WikiTree profile controls to the Person Editor."""
    grid = editor.top.get_object("table3")

    if grid is None:
        return

    label = Gtk.Label(label="WikiTree ID:")
    label.set_halign(Gtk.Align.START)
    label.set_margin_start(6)
    label.set_margin_end(6)

    entry = Gtk.Entry()
    entry.set_hexpand(True)
    entry.set_tooltip_text(
        "WikiTree profile ID, for example Smith-12345"
    )
    entry.set_text(_get_wikitree_id(editor.obj))

    button = Gtk.Button(label="Open WikiTree")
    button.set_tooltip_text(
        "Open this person's profile on WikiTree"
    )

    grid.attach(label, 0, 8, 2, 1)
    grid.attach(entry, 2, 8, 5, 1)
    grid.attach(button, 7, 8, 2, 1)

    editor.wikitree_id_entry = entry
    editor.wikitree_open_button = button

    entry.connect(
        "changed",
        _entry_changed,
        button,
    )
    entry.connect(
        "focus-out-event",
        _entry_focus_out,
    )
    button.connect(
        "clicked",
        _open_wikitree,
        editor,
    )

    _entry_changed(entry, button)

    label.show()
    entry.show()
    button.show()


def _patched_post_init(self):
    """Run the normal Person Editor setup, then add WikiTree controls."""
    _original_post_init(self)
    _add_wikitree_field(self)


def _patched_save(self, *args):
    """Validate and store the WikiTree ID before saving the person."""
    entry = getattr(self, "wikitree_id_entry", None)

    if entry is not None:
        value = _normalize_wikitree_id(entry.get_text())

        if value and not ID_RE.fullmatch(value):
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Invalid WikiTree ID",
            )

            dialog.format_secondary_text(
                "Enter a WikiTree ID such as Smith-12345, "
                "or paste a WikiTree profile URL."
            )

            dialog.run()
            dialog.destroy()
            return

        _set_wikitree_id(self.obj, value)

    return _original_save(self, *args)


def _install_patch():
    """Install the WikiTree Person Editor integration."""
    global _patched
    global _original_post_init
    global _original_save

    if _patched:
        return

    _original_post_init = EditPerson._post_init
    _original_save = EditPerson.save

    EditPerson._post_init = _patched_post_init
    EditPerson.save = _patched_save

    _patched = True


def load_on_reg(dbstate, uistate, plugin):
    """Load WikiTree for Gramps."""
    _install_patch()
    return None