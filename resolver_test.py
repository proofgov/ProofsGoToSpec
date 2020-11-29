# to run
# python resolver_test.py

import unittest

try:
    from .resolver import Resolver
except (ImportError, ValueError):
    from resolver import Resolver


class ResolverTest(unittest.TestCase):
    def test_is_spec_returns_true(self):
        file = "/spec/foo/something_spec.rb"
        r = Resolver().is_spec(file)
        self.assertEqual(r, True)

    def test_is_spec_returns_true_for_erb_spec(self):
        file = "/spec/views/something.html.erb_spec.rb"
        r = Resolver().is_spec(file)
        self.assertEqual(r, True)

    def test_is_spec_returns_true_for_py_spec(self):
        file = "/test/views/something_test.py"
        r = Resolver().is_spec(file, spec_ends_with="test")
        self.assertEqual(r, True)

    def test_is_spec_returns_false(self):
        file = "/app/foo/something.rb"
        r = Resolver().is_spec(file)
        self.assertEqual(r, False)

    def test_is_spec_returns_false_for_erb(self):
        file = "/spec/views/something.html.erb.rb"
        r = Resolver().is_spec(file)
        self.assertEqual(r, False)

    def test_is_spec_returns_false_for_jbuilder(self):
        file = "/spec/views/something.json.jbuilder"
        r = Resolver().is_spec(file)
        self.assertEqual(r, False)

    def test_is_spec_returns_false_for_py_spec(self):
        file = "/test/views/something.py"
        r = Resolver().is_spec(file, spec_ends_with="test")
        self.assertEqual(r, False)

    # get_source
    def test_finds_source(self):
        file = "/spec/something/foo_spec.rb"
        r = Resolver().get_source(file)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/something/foo.rb")
        self.assertEqual(r[1], "/something/foo.rb")

    def test_finds_source_from_erb(self):
        file = "/spec/views/namespace/users/_something.html.erb_spec.rb"
        r = Resolver().get_source(file)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/views/namespace/users/_something.html.erb")
        self.assertEqual(r[1], "/views/namespace/users/_something.html.erb")

    def test_finds_source_from_haml(self):
        file = "/spec/views/documents/update.html.haml_spec.rb"
        r = Resolver().get_source(file)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/views/documents/update.html.haml")
        self.assertEqual(r[1], "/views/documents/update.html.haml")

    def test_finds_source_from_jbuilder(self):
        file = "/spec/views/documents/show.json.jbuilder_spec.rb"
        r = Resolver().get_source(file)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/views/documents/show.json.jbuilder")
        self.assertEqual(r[1], "/views/documents/show.json.jbuilder")

    def test_finds_source_from_lib(self):
        file = "/spec/lib/something/foo_spec.rb"
        r = Resolver().get_source(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/lib/something/foo.rb")

    def test_finds_source_from_js_component_folder(self):
        file = "/test/js/components/FileRenamePrompt-test.js"
        r = Resolver().get_source(file, spec_folder="test")
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/javascript/components/FileRenamePrompt.vue")
        self.assertEqual(r[1], "/javascript/components/FileRenamePrompt.vue")

    def test_finds_source_for_noncomponent(self):
        file = "/test/js/utils/string-utils-test.js"
        r = Resolver().get_source(file, spec_folder="test")
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/javascript/utils/string-utils.js")

    def test_finds_source_from_py(self):
        file = "/tests/something/foo_test.py"
        r = Resolver().get_source(file, spec_folder="tests")
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/something/foo.py")
        self.assertEqual(r[1], "/something/foo.py")

    # get_spec
    def test_finds_spec(self):
        file = "/app/models/user.rb"
        r = Resolver().get_spec(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/models/user_spec.rb")

    def test_finds_spec_from_lib(self):
        file = "/lib/foo/utility.rb"
        r = Resolver().get_spec(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/lib/foo/utility_spec.rb")

    def test_finds_spec_from_erb(self):
        file = "/app/views/users/new.html.erb"
        r = Resolver().get_spec(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/views/users/new.html.erb_spec.rb")

    def test_finds_spec_from_haml(self):
        file = "/app/views/account/login.html.haml"
        r = Resolver().get_spec(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/views/account/login.html.haml_spec.rb")

    def test_finds_spec_from_jbuilder(self):
        file = "/app/views/account/show.json.jbuilder"
        r = Resolver().get_spec(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/views/account/show.json.jbuilder_spec.rb")

    def test_finds_spec_from_other(self):
        file = "/foo/user.rb"
        r = Resolver().get_spec(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/foo/user_spec.rb")

    def test_finds_spec_from_vue(self):
        file = "/app/javascript/components/FileRenamePrompt.vue"
        r = Resolver().get_spec(file, spec_folder="test")
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/test/js/components/FileRenamePrompt-test.js")

    def test_finds_spec_from_py(self):
        file = "/app/something/foo.py"
        r = Resolver().get_spec(file, spec_folder="tests")
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/tests/something/foo_test.py")

    # run
    # returns either the source or spec depending on the given file
    def test_run(self):
        file = "/app/decorators/namespace/user_decorator.rb"
        r = Resolver().run(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/decorators/namespace/user_decorator_spec.rb")

    def test_run_from_lib(self):
        file = "/lib/utilities/namespace/foo.rb"
        r = Resolver().run(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/spec/lib/utilities/namespace/foo_spec.rb")

    def test_run_from_spec(self):
        file = "/spec/controllers/namespace/foo_controller_spec.rb"
        r = Resolver().run(file)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/controllers/namespace/foo_controller.rb")
        self.assertEqual(r[1], "/controllers/namespace/foo_controller.rb")

    def test_run_from_spec_lib(self):
        file = "/spec/lib/namespace/foo_spec.rb"
        r = Resolver().run(file)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], "/lib/namespace/foo.rb")

    def test_run_for_erb_spec(self):
        file = "/spec/views/namespace/users/_new.html.erb_spec.rb"
        r = Resolver().run(file)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/views/namespace/users/_new.html.erb")
        self.assertEqual(r[1], "/views/namespace/users/_new.html.erb")

    def test_run_for_jbuilder_spec(self):
        file = "/spec/views/namespace/users/show.json.jbuilder_spec.rb"
        r = Resolver().run(file)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/views/namespace/users/show.json.jbuilder")
        self.assertEqual(r[1], "/views/namespace/users/show.json.jbuilder")

    def test_run_for_python_spec(self):
        file = "/tests/something/file_test.py"
        r = Resolver().run(file, spec_folder="tests", spec_ends_with="test")
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], "/app/something/file.py")
        self.assertEqual(r[1], "/something/file.py")


if __name__ == "__main__":
    unittest.main()
