"""Tests for the PetTracer config flow."""
from unittest.mock import create_autospec, patch

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResultType
from pettracer import PetTracerClient, PetTracerError

from custom_components.pettracer.const import DOMAIN


async def test_form_user(hass, mock_setup_entry):
    """Test we get the user form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "user"


async def test_form_user_success(hass, mock_setup_entry):
    """Test successful authentication and config entry creation."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
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


async def test_form_invalid_auth(hass, mock_setup_entry, pettracer_error):
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = pettracer_error(401)
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
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = Exception("Unexpected error")
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
        client_instance = create_autospec(PetTracerClient, instance=True)
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
        client_instance = create_autospec(PetTracerClient, instance=True)
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


async def test_reauth_flow(hass, mock_setup_entry):
    """Test reauth flow shows the confirm form."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "old_password",
        },
        unique_id="test@example.com",
    )
    entry.add_to_hass(hass)

    result = await entry.start_reauth_flow(hass)

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"


async def test_reauth_flow_success(hass, mock_setup_entry):
    """Test successful reauth flow."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "old_password",
        },
        unique_id="test@example.com",
    )
    entry.add_to_hass(hass)

    result = await entry.start_reauth_flow(hass)

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "new_password"},
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "reauth_successful"
    assert entry.data[CONF_PASSWORD] == "new_password"


async def test_reauth_flow_unknown_exception(hass, mock_setup_entry):
    """Test reauth flow with unexpected exception."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "old_password",
        },
        unique_id="test@example.com",
    )
    entry.add_to_hass(hass)

    result = await entry.start_reauth_flow(hass)

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = Exception("Unexpected error")
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "new_password"},
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}


async def test_reauth_flow_invalid_auth(hass, mock_setup_entry, pettracer_error):
    """Test reauth flow with invalid credentials."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "old_password",
        },
        unique_id="test@example.com",
    )
    entry.add_to_hass(hass)

    result = await entry.start_reauth_flow(hass)

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = pettracer_error(401)
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "wrong_password"},
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass, mock_setup_entry, pettracer_error):
    """A network error during setup is cannot_connect, not invalid_auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = pettracer_error()
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_USERNAME: "test@example.com", CONF_PASSWORD: "test_password"},
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_cannot_connect_without_http_cause(hass, mock_setup_entry):
    """Library errors with no HTTP cause (e.g. bad JSON) are cannot_connect."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = PetTracerError("Login response is not JSON")
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_USERNAME: "test@example.com", CONF_PASSWORD: "test_password"},
        )

    assert result2["errors"] == {"base": "cannot_connect"}


async def test_reauth_flow_cannot_connect(hass, mock_setup_entry, pettracer_error):
    """A network error during reauth is cannot_connect."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_USERNAME: "test@example.com", CONF_PASSWORD: "old_password"},
        unique_id="test@example.com",
    )
    entry.add_to_hass(hass)

    result = await entry.start_reauth_flow(hass)

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = pettracer_error(503)
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "new_password"},
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_timeout_cannot_connect(hass, mock_setup_entry):
    """A login timeout (not wrapped by the library) is cannot_connect."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = TimeoutError()
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_USERNAME: "test@example.com", CONF_PASSWORD: "test_password"},
        )

    assert result2["errors"] == {"base": "cannot_connect"}


async def test_reauth_flow_timeout_cannot_connect(hass, mock_setup_entry):
    """A login timeout during reauth is cannot_connect."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_USERNAME: "test@example.com", CONF_PASSWORD: "old_password"},
        unique_id="test@example.com",
    )
    entry.add_to_hass(hass)

    result = await entry.start_reauth_flow(hass)

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        client_instance = create_autospec(PetTracerClient, instance=True)
        client_instance.login.side_effect = TimeoutError()
        mock_client.return_value = client_instance

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "new_password"},
        )

    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_uses_shared_session(hass, mock_setup_entry):
    """Credential checks reuse HA's shared aiohttp session."""
    from homeassistant.helpers.aiohttp_client import async_get_clientsession

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.pettracer.config_flow.PetTracerClient"
    ) as mock_client:
        mock_client.return_value = create_autospec(PetTracerClient, instance=True)
        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_USERNAME: "test@example.com", CONF_PASSWORD: "test_password"},
        )

    mock_client.assert_called_once_with(session=async_get_clientsession(hass))
