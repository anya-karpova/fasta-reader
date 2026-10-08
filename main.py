from pathlib import Path
class Seq:
    """
    Класс для хранения и анализа биологических последовательностей.
    :param header: Заголовок FASTA-записи.
    :type header: str
    :param sequence: Биологическая последовательность.
    :type sequence: str
    """
    def __init__(self, header, sequence):
        """Сохраняет заголовок FASTA и последовательность."""
        self.header = header
        self.sequence = sequence.upper()

    def __len__(self):
        """Возвращает длину последовательности."""
        return len(self.sequence)

    def __str__(self):
        """Возвращает последовательность в формате FASTA."""
        return f">{self.header}\n{self.sequence}"

    def __repr__(self):
        """Возвращает информацию об объекте."""
        return f"Seq({self.header!r}, {self.sequence!r})"

    def get_alphabet(self):
        """Определяет алфавит последовательности."""
        nucleotide = set("ACGTURYSWKMBDHVN")
        protein = set("ACDEFGHIKLMNPQRSTVWYBXZJUO*")
        letters = set(self.sequence)
        if letters.issubset(nucleotide):
            return "нуклеотидная"
        elif letters.issubset(protein):
            return "белковая"
        else:
            return "неизвестная"


class FastaReader:
    """
    Класс для чтения и проверки файлов формата FASTA.
    :param file_path: Путь к FASTA-файлу.
    :type file_path: str
    """
    def __init__(self, file_path):
        """Сохраняет путь к файлу."""
        self.file_path = file_path

    def read(self):
        """Читает FASTA-файл по записям."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            header = None
            sequence_parts = []
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    if header is not None:
                        if not sequence_parts:
                            raise ValueError("У записи нет последовательности")
                        yield Seq(header, "".join(sequence_parts))
                    header = line[1:].strip()
                    if not header:
                        raise ValueError("Пустой заголовок FASTA")
                    sequence_parts = []
                else:
                    if header is None:
                        raise ValueError("Последовательность находится до заголовка")
                    sequence_parts.append(line)
            if header is None:
                raise ValueError("Файл FASTA пустой")
            if not sequence_parts:
                raise ValueError("У записи нет последовательности")
            yield Seq(header, "".join(sequence_parts))

    def is_fasta(self):
        """Проверяет структуру FASTA-файла."""
        try:
            for record in self.read():
                pass
            return True
        except (ValueError, OSError, UnicodeError):
            return False


if __name__ == "__main__":
    reader = FastaReader("example.fasta")
    try:
        for seq in reader.read():
            print(seq)
            print("Длина:", len(seq))
            print("Тип:", seq.get_alphabet())
            print()
    except Exception as error:
        print("Ошибка:", type(error).__name__, error)
    print("Проверка формата FASTA:", reader.is_fasta())
    invalid_reader = FastaReader("invalid.fasta")
    print("Проверка неправильного FASTA:", invalid_reader.is_fasta())

    if __name__ == "__main__":
     folder = Path(__file__).resolve().parent
    reader = FastaReader(folder / "example.fasta")
    try:
        for seq in reader.read():
            print(seq)
            print("Длина:", len(seq))
            print("Тип:", seq.get_alphabet())
            print()
    except Exception as error:
        print("Ошибка:", type(error).__name__, error)
    print("Проверка формата FASTA:", reader.is_fasta())
    invalid_reader = FastaReader(folder / "invalid.fasta")
    print("Проверка неправильного FASTA:", invalid_reader.is_fasta())