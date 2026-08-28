from django.contrib.gis import forms as gisforms

from tests.base import BootstrapTestCase


class GisTestForm(gisforms.Form):
    point = gisforms.PointField()


# A geometry widget builds its own template context from `attrs`. Django ticket #28105
# was a crash in that path, triggered by a template pack passing an attr whose name the
# widget already used. These tests guard that seam.
class GisFieldTestCase(BootstrapTestCase):
    """Test rendering of `django.contrib.gis` form fields."""

    def test_gis_point(self):
        """Test field with a GIS point widget."""
        html = self.render("{% bootstrap_field form.point %}", context={"form": GisTestForm()})
        self.assertInHTML('<label class="form-label" for="id_point">Point</label>', html)
        # The geometry widget renders its own map markup; the serialized value is a
        # hidden textarea that keeps the widget's own classes rather than form-control.
        self.assertIn('id="id_point_div_map"', html)
        self.assertIn('class="vSerializedField required"', html)
        self.assertNotIn("form-control", html)

    def test_gis_point_horizontal(self):
        """Test field with a GIS point widget in horizontal layout."""
        html = self.render('{% bootstrap_field form.point layout="horizontal" %}', context={"form": GisTestForm()})
        self.assertInHTML('<label class="col-form-label col-sm-2" for="id_point">Point</label>', html)
        self.assertIn('id="id_point_div_map"', html)
