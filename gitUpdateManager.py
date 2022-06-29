from git import Repo

class GitUpdateManager:
    def __init__(self) :

        self.repo =  Repo('C:/Work/ViewSqlManager')
        for remote in self.repo.remotes:
            remote.fetch()
        self.state = self.repo.git.status()

    def need_update(self) -> bool :

        control = str(self.state)
        updated= "Your branch is up to date"

        if updated not in control:
            return True
        else:
            return False

    def updater(self) :

        self.repo.remotes.origin.pull()
