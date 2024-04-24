from qgis.PyQt.QtWidgets import QPlainTextEdit

from zonal_exact.user_communication import WidgetPlainTextWriter


def test_init_widget_plain_text():
    plain_text_edit = QPlainTextEdit()

    widget_plain_text = WidgetPlainTextWriter(plain_text_widget=plain_text_edit)

    assert isinstance(widget_plain_text.plain_text_widget, QPlainTextEdit)


def test_write_info():
    plain_text_edit = QPlainTextEdit()

    msg = "example info message"
    widget_plain_text = WidgetPlainTextWriter(plain_text_widget=plain_text_edit)
    widget_plain_text.write_info(msg=msg)

    output_content = widget_plain_text.plain_text_widget.toPlainText()
    assert output_content == f"[INFO]: {msg}"


def test_write_warn():
    plain_text_edit = QPlainTextEdit()

    msg = "example warn message"
    widget_plain_text = WidgetPlainTextWriter(plain_text_widget=plain_text_edit)
    widget_plain_text.write_warn(msg=msg)

    output_content = widget_plain_text.plain_text_widget.toPlainText()
    assert output_content == f"[WARNING]: {msg}"


def test_write_error():
    plain_text_edit = QPlainTextEdit()

    msg = "example error message"
    widget_plain_text = WidgetPlainTextWriter(plain_text_widget=plain_text_edit)
    widget_plain_text.write_error(msg=msg)

    output_content = widget_plain_text.plain_text_widget.toPlainText()
    assert output_content == f"[ERROR]: {msg}"
