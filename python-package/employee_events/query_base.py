# Import any dependencies needed to execute sql queries
from .sql_execution import QueryMixin


# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
class QueryBase(QueryMixin):
    """Queries shared by the employee and team tables."""

    # Create a class attribute called `name`
    # set the attribute to an empty string
    name = ""

    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        """Return the (name, id) pairs for this table. Empty by default."""

        # Return an empty list
        return []

    @staticmethod
    def validate_id(id):
        """Return the id as an integer, or raise ValueError.

        The queries place the id inside the SQL text, so only
        whole numbers are accepted. This stops any other text
        from being run as SQL.
        """
        text = str(id).strip()
        if not text.isdigit():
            raise ValueError(f"id must be a whole number, got {id!r}")
        return int(text)

    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id):
        """Return daily positive and negative event totals for one id."""

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        id = self.validate_id(id)
        return self.pandas_query(f"""
            SELECT event_date
                 , SUM(positive_events) AS positive_events
                 , SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date
        """)

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id):
        """Return the manager notes recorded for one id."""

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        id = self.validate_id(id)
        return self.pandas_query(f"""
            SELECT note_date
                 , note
            FROM notes
            JOIN {self.name}
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
            ORDER BY note_date
        """)
