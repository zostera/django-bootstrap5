from tests.base import BootstrapTestCase


class BootstrapLabelTestCase(BootstrapTestCase):
    def test_bootstrap_label(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_label "Subject" %}'),
            '<label class="form-label">Subject</label>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_for='subject' %}"),
            '<label for="subject" class="form-label">Subject</label>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_class='label-class' %}"),
            '<label class="label-class">Subject</label>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_title='label-title' %}"),
            '<label title="label-title" class="form-label">Subject</label>',
        )

    def test_show_label_true(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_label "Subject" show_label=True %}'),
            '<label class="form-label">Subject</label>',
        )

    def test_show_label_false(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_label "Subject" show_label=False %}'),
            '<label class="visually-hidden">Subject</label>',
        )

    def test_show_label_empty(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" show_label='' %}"),
            '<label class="visually-hidden">Subject</label>',
        )

    def test_show_label_visually_hidden(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" show_label='visually-hidden' %}"),
            '<label class="visually-hidden">Subject</label>',
        )

    def test_show_label_visually_hidden_keeps_label_class(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_class='label-class' show_label=False %}"),
            '<label class="label-class visually-hidden">Subject</label>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_class='label-class' show_label='visually-hidden' %}"),
            '<label class="label-class visually-hidden">Subject</label>',
        )

    def test_show_label_visually_hidden_keeps_other_attributes(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_for='subject' show_label=False %}"),
            '<label for="subject" class="visually-hidden">Subject</label>',
        )

    def test_show_label_skip(self):
        self.assertEqual(
            self.render("{% bootstrap_label \"Subject\" label_for='subject' show_label='skip' %}"),
            "",
        )
