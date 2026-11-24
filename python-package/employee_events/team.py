# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies for sql execution
# (The `query` and `pandas_query` methods come from `QueryMixin`,
# which `QueryBase` already inherits, so the mixin is not added
# to this class a second time.)


# Create a subclass of QueryBase
# called  `Team`
class Team(QueryBase):
    """Queries for a team of employees."""

    # Set the class attribute `name`
    # to the string "team"
    name = "team"

    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
    def names(self):
        """Return (team name, team id) for every team."""

        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
        return self.query("""
            SELECT team_name
                 , team_id
            FROM team
        """)

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
    def username(self, id):
        """Return the name of the team with the given id."""

        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
        id = self.validate_id(id)
        return self.query(f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """)

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    def model_data(self, id):
        """Return the model features for each employee on one team."""
        id = self.validate_id(id)

        return self.pandas_query(f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """)
