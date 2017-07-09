import py2neo #Libs to connect to neo4j

def connectDb():
    """Function to connect to neo4j database."""

    py2neo.authenticate("localhost:7474", "neo4j", "lucas")
    dbConnection = py2neo.Graph("http://localhost:7474/db/data/")

    return dbConnection

dbConnection = connectDb()



def createNodeQuery(**kwargs):
    query = "MATCH (n:{})".format(kwargs['label'])
    del kwargs['label']

    if len(kwargs) > 0:
        query += " WHERE "
  
    where_clauses = list()
    for key, value in kwargs.items():
        where_clauses.append("n.{} = '{}'".format(key, value))

    query += " AND ".join(where_clauses) + " RETURN n"

    return query

class neo4jModel(object):

    def __init__(self, **kwargs):
        

    @classmethod
    def get(cls, **kwargs):
        model_label = cls.__name__
        kwargs['label'] = model_label
        db_query = createNodeQuery(**kwargs)
        print(db_query)

        for result in dbConnection.run(db_query):
            return result

        raise cls.DoesNotExist()

    class DoesNotExist(Exception):
        pass

    # @classmethod
    # def getClassName(cls):
    #     return cls.__name__

# neo4jModel.objects = 


class WikiArticle(neo4jModel):
    pass
    # title = models.CharField(max_length=200, unique=True)
    # pageid = models.IntegerField()
    # links = models.ManyToManyField('ArticleLink')

    # def __str__(self):
    #     return self.__class__

class ArticleLink(neo4jModel):
    # link = models.ForeignKey("WikiUrl")
    # score = models.FloatField()

    def __str__(self):
        return self.link.url

class WikiUrl(neo4jModel):
    # url = models.CharField(max_length=200, unique=True)
    # article = models.ForeignKey("WikiArticle", null=True)

    def __str__(self):
        return self.url


if __name__ == "__main__":
    article = WikiArticle.get(title="lucas").title
    print()
