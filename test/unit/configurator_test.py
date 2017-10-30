# encoding: utf-8
import pytest

from lutece.configurator import AssetConfigurator


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def build_dummy_app(content):
    from contextlib import contextmanager
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    class DummyApp(object):
        # pylint: disable=no-self-use
        @contextmanager
        def open_resource(self, _manifest_file, _mode):
            if isinstance(content, str):
                yield StringIO(content)
            else:
                raise IOError

        def add_template_global(self, _fun):
            pass

    return DummyApp()


def test_built_asset_file_with_missing_manifest_json():
    manifest_json = 'manifest.json'
    configurator = AssetConfigurator(manifest_json)

    dummy_app = build_dummy_app(None)  # IOError
    configurator.init_app(dummy_app)

    assert {} == configurator.assets
    assert 'file.css' == configurator.built_asset_file('file.css')


def test_built_asset_file_with_empty_manifest_json():
    manifest_json = 'manifest.json'
    configurator = AssetConfigurator(manifest_json)

    dummy_app = build_dummy_app('{}')
    configurator.init_app(dummy_app)

    assert {} == configurator.assets
    assert 'file.css' == configurator.built_asset_file('file.css')


def test_built_asset_file_with_valid_manifest_json():
    manifest_json = 'manifest.json'
    configurator = AssetConfigurator(manifest_json)

    content = """{
"file.css": "file-123.css",
"file.js": "file.abc.js"
}"""
    dummy_app = build_dummy_app(content)
    configurator.init_app(dummy_app)

    assert {
        'file.css': 'file-123.css',
        'file.js': 'file.abc.js'} == configurator.assets
    assert 'file-123.css' == configurator.built_asset_file('file.css')
    assert 'file.abc.js' == configurator.built_asset_file('file.js')
