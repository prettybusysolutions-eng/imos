from imos.services.entity_linker import EntityLinker

def test_linker_runs():
    out = EntityLinker().link_same_name()
    assert 'links_created' in out

