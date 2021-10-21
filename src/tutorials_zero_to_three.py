
metadata_obj = MetaData()

genome_table = Table(
    "genome",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('rsid_number', String(30)),
    Column('chromosome', Integer),
    Column('genotype', String(2))
)

# genome_table.c.keys() = ['id', 'rsid_number', 'chromosome', 'genotype']

metadata_obj.create_all(engine)  # Creates all tables defined in our metadata_obj

# Basic connection "commit-as-you-go"
# with engine.connect() as conn:
    # Basic access
    # result = conn.execute(text("select 'hello world'"))
    # print(result.all())

    # Committing Changes
    # conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    # conn.execute(
    #     text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
    #     [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    # )
    # conn.commit()

# "Begin once" transactional commit
# with engine.begin() as conn:
#     conn.execute(
#         text("INSERT INTO some_table (x,y) VALUES (:x, :y)"),
#         [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
#     )
#
#     result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 1})
#     # conn.execute() returns an iterable
#     for row in result:
#         print(f"x: {row.x}, y: {row.y}")


# Session based commits
# stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=1)
# with Session(engine) as session:
#     result = session.execute(stmt)
#     for row in result:
#         print(f"x: {row.x}\ty: {row.y}")
#     session.commit()

