import re

RUBY_SPEC_MATCHER = re.compile(r"_spec\.rb$")
RUBY_SOUCE_MATCHER = re.compile(r"\.rb$")
RUBY_SPECIAL_SPEC_MATCHER = re.compile(r"(\.erb|\.haml|\.slim|\.jbuilder)_spec\.rb$")
RUBY_SPECIAL_SOURCE_MATCHER = re.compile(r"\.erb$|\.haml$|\.slim$|\.jbuilder$")
JS_SPEC_MATCHER = re.compile(r"-test\.js$")
PYTHON_SPEC_MATCHER = re.compile(r"_test\.py$")
PYTHON_COURCE_MATCHER = re.compile(r"\.py$")


class Resolver:
    def run(self, file, spec_folder="spec", spec_ends_with="spec"):
        if self.is_spec(file, spec_ends_with=spec_ends_with):
            return self.get_source(file, spec_folder=spec_folder)

        return self.get_spec(file, spec_folder=spec_folder)

    def is_spec(self, file, spec_ends_with="spec"):
        file_without_extestion = file.rsplit(".", 1)[0]
        return file_without_extestion.endswith(spec_ends_with)

    def get_source(self, file, spec_folder="spec"):
        related = []

        # find erb, haml
        if RUBY_SPECIAL_SPEC_MATCHER.search(file):
            match = RUBY_SPECIAL_SPEC_MATCHER.search(file)
            source_ext = match.group(1)
            file = RUBY_SPECIAL_SPEC_MATCHER.sub(source_ext, file)
        elif RUBY_SPEC_MATCHER.search(file):
            # simply sub .rb to _spec.rb
            # e.g. foo.rb -> foo_spec.rb
            file = RUBY_SPEC_MATCHER.sub(".rb", file)
        elif PYTHON_SPEC_MATCHER.search(file):
            file = PYTHON_SPEC_MATCHER.sub(".py", file)

        if file.find("/" + spec_folder + "/lib/") > -1:
            # file in lib
            related.append(re.sub(r"/" + spec_folder + "/lib/", "/lib/", file))
        else:
            related.append(re.sub(r"/" + spec_folder + "/", "/app/", file, 1))
            related.append(re.sub(r"/" + spec_folder + "/", "/", file, 1))

        # js/vue matchers
        if JS_SPEC_MATCHER.search(file):
            match = JS_SPEC_MATCHER.search(file)
            for index, file in enumerate(related):
                related[index] = self.patch_js_source(related[index], match)

        return related

    def get_spec(self, file, spec_folder="spec"):
        related = []

        if RUBY_SOUCE_MATCHER.search(file):
            file = RUBY_SOUCE_MATCHER.sub("_spec.rb", file)
        elif RUBY_SPECIAL_SOURCE_MATCHER.search(file):
            # find erb, haml
            match = RUBY_SPECIAL_SOURCE_MATCHER.search(file)
            ext = match.group(0)
            regex = re.compile(re.escape(ext) + "$")
            file = regex.sub(ext + "_spec.rb", file)
        elif PYTHON_COURCE_MATCHER.search(file):
            file = PYTHON_COURCE_MATCHER.sub("_test.py", file)

        if file.find("/lib/") > -1:
            related.append(re.sub(r"/lib/", "/" + spec_folder + "/lib/", file))
        elif file.find("/app/") > -1:
            related.append(re.sub(r"/app/", "/" + spec_folder + "/", file, 1))
        else:
            related.append("/" + spec_folder + file)

        # js/vue matchers
        match = re.search(r".js$|.vue$", file)
        if match:
            related[0] = self.patch_js_spec(related[0], match)

        return related

    def patch_js_spec(self, file, match):
        ext = match.group(0)
        regex = re.escape(ext) + "$"
        file = re.sub(regex, "-test.js", file, 1)
        file = re.sub(r"/javascript/", "/js/", file, 1)
        return file

    def patch_js_source(self, file, match):
        ext = match.group(0)
        regex = re.escape(ext) + "$"
        ext = ".js"
        if re.search("/components/", file):
            ext = ".vue"
        file = re.sub(regex, ext, file, 1)
        file = re.sub(r"/js/", "/javascript/", file, 1)
        return file
