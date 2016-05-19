
from colab.plugins.data import PluginDataImporter


class ColabDiscoursePluginDataImporter(PluginDataImporter):
    app_label = 'colab_discourse'

    def fetch_data(self):
        pass
