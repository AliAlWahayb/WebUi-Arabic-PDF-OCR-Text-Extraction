from .__base import FarasaBase


class FarasaStemmer(FarasaBase):
    task = "stem"

    @property
    def command(self):
        if self.bin_path is not None:
            return self.BASE_CMD + [str(self.bin_path)]
        return self.BASE_CMD + [
            str(self.bin_dir / "lib" / "FarasaSegmenterJar.jar"),
            "-l",
            "true",
        ]

    def stem(self, text):
        return self.do_task(text=text)
