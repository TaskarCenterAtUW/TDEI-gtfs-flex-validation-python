# in an effort to be more permissive of small errors, accept these which could conceivably be calculated/fixed/interpreted by common applications
CHANGE_ERROR_TO_WARNING = [
    'block_trips_with_overlapping_stop_times',
    'trip_distance_exceeds_shape_distance',
    'decreasing_or_equal_stop_time_distance',
    'decreasing_shape_distance',
    'empty_file',
    'equal_shape_distance_diff_coordinates',
    'fare_transfer_rule_duration_limit_type_without_duration_limit',
    'fare_transfer_rule_duration_limit_without_type',
    'fare_transfer_rule_invalid_transfer_count',
    'fare_transfer_rule_missing_transfer_count',
    'fare_transfer_rule_with_forbidden_transfer_count',
    'forbidden_shape_dist_traveled',
    'invalid_currency',
    'invalid_currency_amount',
    'invalid_url',
    'location_with_unexpected_stop_time',
    'missing_trip_edge',
    'new_line_in_value',
    'point_near_origin',
    'point_near_pole',
    'route_both_short_and_long_name_missing',
    'route_networks_specified_in_more_than_one_file',
    'start_and_end_range_equal',
    'start_and_end_range_out_of_order',
    'station_with_parent_station',
    'stop_time_timepoint_without_times',
    'stop_time_with_arrival_before_previous_departure_time',
    'stop_time_with_only_arrival_or_departure_time',
    'stop_without_location',
    'timeframe_only_start_or_end_time_specified',
    'timeframe_overlap',
    'timeframe_start_or_end_time_greater_than_twenty_four_hours',
    'u_r_i_syntax_error'
]

FLEX_FATAL_ERROR_CODES = [
    'missing_required_element',
    'unsupported_feature_type',
    'unsupported_geo_json_type',
    'unsupported_geometry_type',
    'invalid_geometry',
    'forbidden_prior_day_booking_field_value',
    'forbidden_prior_notice_start_day',
    'forbidden_prior_notice_start_time',
    'forbidden_real_time_booking_field_value',
    'forbidden_same_day_booking_field_value',
    'invalid_prior_notice_duration_min',
    'missing_prior_day_booking_field_value',
    'missing_prior_notice_duration_min',
    'missing_prior_notice_start_time',
    'prior_notice_last_day_after_start_day'
]

FLEX_FIELDS = {
    'stop_times.txt': [
        'start_pickup_dropoff_window',
        'end_pickup_dropoff_window',
        'pickup_booking_rule_id',
        'drop_off_booking_rule_id',
        'mean_duration_factor',
        'mean_duration_offset',
        'safe_duration_factor',
        'safe_duration_offset'
    ]
}

FLEX_FILES = [
    'locations.geojson',
    'booking_rules.txt',
    'location_groups.txt',
    'location_group_stops.txt'

]
