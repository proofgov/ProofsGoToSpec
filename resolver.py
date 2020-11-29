import re

RUBY_SPEC_MATCHER = re.compile(r"_spec\.rb$")
RUBY_SOUCE_MATCHER = re.compile(r"\.rb$")
RUBY_SPECIAL_SPEC_MATCHER = re.compile(r"(\.erb|\.haml|\.slim|\.jbuilder)_spec\.rb$")
RUBY_SPECIAL_SOURCE_MATCHER = re.compile(r"\.erb$|\.haml$|\.slim$|\.jbuilder$")
JS_SPEC_MATCHER = re.compile(r"-test\.js$")
PYTHON_SPEC_MATCHER = re.compile(r"_test\.py$")


class Resolver:
    def run(self, file, spec_base="spec"):
        if self.is_spec(file, spec_base):
            return self.get_source(file, spec_base)
        else:
            return self.get_spec(file, spec_base)

    def is_spec(self, file, spec_base="spec"):
        file_without_extestion = file.rsplit(".", 1)[0]
        return file_without_extestion.endswith(spec_base)

    def get_source(self, file, spec_root="spec"):
        related = []

        if RUBY_SPEC_MATCHER.search(file):
            # find erb, haml
            match = RUBY_SPECIAL_SPEC_MATCHER.search(file)
            if match:
                source_ext = match.group(1)
                file = RUBY_SPECIAL_SPEC_MATCHER.sub(source_ext, file)
            else:
                # simply sub .rb to _spec.rb
                # e.g. foo.rb -> foo_spec.rb
                file = RUBY_SPEC_MATCHER.sub(".rb", file)
        elif PYTHON_SPEC_MATCHER.search(file):
            file = PYTHON_SPEC_MATCHER.sub(".py", file)

        if file.find("/" + spec_root + "/lib/") > -1:
            # file in lib
            related.append(re.sub(r"/" + spec_root + "/lib/", "/lib/", file))
        else:
            related.append(re.sub(r"/" + spec_root + "/", "/app/", file, 1))
            related.append(re.sub(r"/" + spec_root + "/", "/", file, 1))

        # js/vue matchers
        if JS_SPEC_MATCHER.search(file):
            match = JS_SPEC_MATCHER.search(file)
            for index, file in enumerate(related):
                related[index] = self.patch_js_source(related[index], match)

        return related

    def get_spec(self, file, spec_root="spec"):
        related = []

        if RUBY_SOUCE_MATCHER.search(file):
            file = RUBY_SOUCE_MATCHER.sub("_spec.rb", file)
        elif RUBY_SPECIAL_SOURCE_MATCHER.search(file):
            # find erb, haml
            match = RUBY_SPECIAL_SOURCE_MATCHER.search(file)
            ext = match.group(0)
            regex = re.compile(re.escape(ext) + "$")
            file = regex.sub(ext + "_spec.rb", file)

        if file.find("/lib/") > -1:
            related.append(re.sub(r"/lib/", "/" + spec_root + "/lib/", file))
        elif file.find("/app/") > -1:
            related.append(re.sub(r"/app/", "/" + spec_root + "/", file, 1))
        else:
            related.append("/" + spec_root + file)

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
