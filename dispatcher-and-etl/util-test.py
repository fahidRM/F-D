import pytest
import re
import arrow
import util

def test_is_uuid():
    assert util.is_uuid('123e4567-e89b-12d3-a456-426614174000')
    assert not util.is_uuid('not-a-uuid')
    assert not util.is_uuid('123e4567e89b12d3a456426614174000')

def test_is_valid_name():
    assert util.is_valid_name('John Doe')
    assert util.is_valid_name("O'Connor")
    assert not util.is_valid_name('')
    assert not util.is_valid_name('John123')

def test_is_valid_email():
    assert util.is_valid_email('test@example.com')
    assert util.is_valid_email('user.name+tag@domain.co.uk')
    assert not util.is_valid_email('not-an-email')
    assert not util.is_valid_email('user@.com')

def test_is_valid_instagram_handle():
    assert util.is_valid_instagram_handle('@valid_handle')
    assert util.is_valid_instagram_handle('valid.handle')
    assert not util.is_valid_instagram_handle('invalid..handle')
    assert not util.is_valid_instagram_handle('toolong' * 5)

def test_is_valid_tiktok_handle():
    assert util.is_valid_tiktok_handle('@validhandle')
    assert util.is_valid_tiktok_handle('valid_handle')
    assert not util.is_valid_tiktok_handle('a')
    assert not util.is_valid_tiktok_handle('toolonghandletoolonghandletoolong')

def test_is_valid_platform():
    assert util.is_valid_platform('Instagram')
    assert util.is_valid_platform('TikTok')
    assert not util.is_valid_platform('MySpace')

def test_format_date():
    date_str = '2024-06-01T15:30:00+05:30'
    formatted = util.format_date(date_str)
    assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{2}:\d{2}$', formatted)

def test_is_valid_date():
    assert util.is_valid_date('2024-06-01T15:30:00+05:30')
    assert util.is_valid_date('2024-06-01')
    assert not util.is_valid_date('not-a-date')
    assert not util.is_valid_date(None)

def test_is_valid_url():
    assert util.is_valid_url('http://example.com')
    assert util.is_valid_url('https://example.com/path')
    assert not util.is_valid_url('ftp:/example.com')
    assert not util.is_valid_url('example.com')
