def test_required_health_states_are_defined():
    required = {'HEALTHY', 'DEGRADED', 'SYSTEM_HALTED'}
    assert required == {'HEALTHY', 'DEGRADED', 'SYSTEM_HALTED'}
