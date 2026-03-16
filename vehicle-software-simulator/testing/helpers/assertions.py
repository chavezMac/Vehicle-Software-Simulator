def assert_has_keys(snapshot, keys):
    payload = snapshot.get("payload", snapshot)
    for key in keys:
        assert key in payload

def assert_changed(snapshots, field):
    values = []
    for snapshot in snapshots:
        payload = snapshot.get("payload", snapshot)
        if field in payload:
            values.append(payload[field])
    assert len(values) > 1
    assert any(v != values[0] for v in values[1:])


def assert_not_stale(snapshots, field, max_stale_sec):
    # compare receive times at points where field value changes
    points = []

    for s in snapshots:
        ts = s['ts_recv']
        payload = s.get("payload", s)
        if field in payload:
            points.append((ts, payload[field]))
        
    assert points, f"No samples found for field '{field}'"

    last_change_ts, last_value = points[0]
    
    for ts, value in points[1:]:
        if value != last_value:
            last_value = value
            last_change_ts = ts
        stale_for = ts - last_change_ts
        assert stale_for <= max_stale_sec, (
            f"{field} stale for {stale_for:.2f}s (> {max_stale_sec}s)"
        )