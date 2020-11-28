import re


class Resolver:
    def run(self, file, spec_base="spec"):
        if self.is_spec(file, spec_base):
            return self.get_source(file, spec_base)
        else:
            return self.get_spec(file, spec_base)

    def is_spec(self, file, spec_base="spec"):
        file_without_extestion = file.rsplit(".", 1)[0]
        return file_without_extestion.endswith(spec_base)

    def get_source(self, file, spec_base="spec"):
        # find erb, haml
        match = re.search(r"(.erb|.haml|.slim|.jbuilder)_spec.rb$", file)
        related = []

        if match:
            ext = match.group(0)
            regex = re.escape(ext)
            ext = re.sub(r"_spec.rb", "", ext)
            file = re.sub(regex, ext, file)
        else:
            # simply sub .rb to _spec.rb
            # e.g. foo.rb -> foo_spec.rb
            file = re.sub(r"\_spec.rb$", ".rb", file)

        if file.find("/" + spec_base + "/lib/") > -1:
            # file in lib
            related.append(re.sub(r"/" + spec_base + "/lib/", "/lib/", file))
        else:
            related.append(re.sub(r"/" + spec_base + "/", "/app/", file, 1))
            related.append(re.sub(r"/" + spec_base + "/", "/", file, 1))

        # js/vue matchers
        match = re.search(r"-test.js$", file)
        if match:
            for index, file in enumerate(related):
                related[index] = self.patch_js_source(related[index], match)

        return related

    def get_spec(self, file, spec_base="spec"):
        # find erb, haml
        match = re.search(r"erb$|haml$|slim$|jbuilder$", file)
        related = []

        if match:
            ext = match.group(0)
            regex = re.escape(ext) + "$"
            file = re.sub(regex, ext + "_spec.rb", file)
        else:
            file = re.sub(r"\.rb$", "_spec.rb", file)

        if file.find("/lib/") > -1:
            related.append(re.sub(r"/lib/", "/" + spec_base + "/lib/", file))
        elif file.find("/app/") > -1:
            related.append(re.sub(r"/app/", "/" + spec_base + "/", file, 1))
        else:
            related.append("/" + spec_base + file)

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
