# Define molecules


class Molecule(object):
    def __init__(self, names=None, iupac=None, cas=None, formula=None, rt=None):
        """
        Creates a molecule

        Keyword arguments:
        names -- List of names the molecules is known by
        iupac -- iupac name of the molecule
        cas -- CAS registry number of the molecule
        formula -- Chemical formula of the molecule
        rt -- Retention time for the molecule
        """
        if names == None:
            names = []

        self.iupac_name = iupac
        self.cas_registry_number = cas
        self.formula = formula
        self.retention_time = rt
        self.names = names

    def __str__(self):
        return f"{self.names} - {self.iupac_name} - {self.formula} - CAS: {self.cas_registry_number} - RT: {self.retention_time}"

    def has_compatible_retention_time(self, other, tolerance=0.5):
        """
        Returns True if the test molecule retention time is within some distance of the
        current molecule retention time.

        If either of the retention_time is None, returns False
        """
        if self.retention_time is None or other.retention_time is None:
            return False

        return abs(self.retention_time - other.retention_time) < tolerance
