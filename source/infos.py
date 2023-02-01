class DocumentInfos:

    title = u'Résolution de sudokus avec la programmation par contraintes'
    first_name = 'Damien'
    last_name = 'Fellmann'
    author = f'{first_name} {last_name}'
    year = u'2023'
    month = u'Janvier'
    seminary_title = u'Travail personnel OCI'
    tutor = u"Cédric Donner"
    release = "(Version finale)"
    repository_url = "https://github.com/<username>/<reponame>"

    @classmethod
    def date(cls):
        return cls.month + " " + cls.year

infos = DocumentInfos()