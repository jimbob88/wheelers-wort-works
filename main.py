import sys
if sys.version_info >= (3, 0):
    import beer_engine
else:
    import beer_engine2 as beer_engine

beer_engine.main()
