"""Mapping of field name and its index in review/defect CSV file."""


review_field_index = {
    'id': 0,
    'review_creation_date': 1,
    'creator_login': 2,
    'creator_full_name': 3,
    'defect_count': 4,
    'comment_count': 5,
    'loc': 6,
    'loc_changed': 7,
    'total_person_time': 8
}


defect_field_index = {
    'defect_id': 0,
    'review_id': 1,
    'review_creation_date': 2,
    'creator_login': 3,
    'creator_full_name': 4,
    'severity': 5,
    'type_cvb': 6,
    'injection_stage': 7
}
