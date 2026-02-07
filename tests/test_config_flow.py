"""Tests for the PetTracer config flow."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pettracer import PetTracerError

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResultType

from custom_components.pettracer.const import DOMAIN


async def test_form_user(hass, mock_setup_entry):
    """Test we get the user form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "user"


async def test_form_user_success(hass, mock_setup_entry, mock_pettracer_client):
    """Test successful authentication and config entry creation."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = MagicMock()
        client_instance.login = AsyncMock()
        mock_client.return_value = client_instance
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "test@example.com",
                CONF_PASSWORD: "test_password",
            },
        )

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "PetTracer (test@example.com)"
    assert result2["data"] == {
        CONF_USERNAME: "test@example.com",
        CONF_PASSWORD: "test_password",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass, mock_setup_entry):
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = MagicMock()
        client_instance.login = AsyncMock(side_effect=PetTracerError("Invalid credentials"))
        mock_client.return_value = client_instance
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "test@example.com",
                CONF_PASSWORD: "wrong_password",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_unknown_exception(hass, mock_setup_entry):
    """Test we handle unknown exceptions."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = MagicMock()
        client_instance.login = AsyncMock(side_effect=Exception("Unexpected error"))
        mock_client.return_value = client_instance
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "test@example.com",
                CONF_PASSWORD: "test_password",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}


async def test_form_duplicate_entry(hass, mock_setup_entry):
    """Test we handle duplicate entries."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry
    
    # Create an existing entry using MockConfigEntry which properly handles async methods
    existing_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "test_password",
        },
        unique_id="test@example.com",
    )
    existing_entry.add_to_hass(hass)
    
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = MagicMock()
        client_instance.login = AsyncMock()
        mock_client.return_value = client_instance
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "test@example.com",
                CONF_PASSWORD: "test_password",
            },
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "already_configured"


async def test_form_case_insensitive_username(hass, mock_setup_entry):
    """Test that usernames are case-insensitive for unique_id."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = MagicMock()
        client_instance.login = AsyncMock()
        mock_client.return_value = client_instance
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "TEST@EXAMPLE.COM",
                CONF_PASSWORD: "test_password",
            },
        )

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    # Verify the unique_id is lowercase
    assert result2["data"][CONF_USERNAME] == "TEST@EXAMPLE.COM"
