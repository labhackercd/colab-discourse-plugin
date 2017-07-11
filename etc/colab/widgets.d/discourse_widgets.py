from colab.widgets.widget_manager import WidgetManager
from colab_discourse.widgets.home_section import DiscourseHomeSectionWidget


WidgetManager.register_widget('home_section', DiscourseHomeSectionWidget())
