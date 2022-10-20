import time

import pyperclip
from playwright.sync_api import expect


def test_dynamic_id(page):
    """Record button click. Then execute your test to make sure that ID is not used for button identification."""
    page.goto("/")
    page.click('text=Dynamic ID')
    page.locator("text=Button with Dynamic ID").click()

    expect(page.locator("text=Button with Dynamic ID")).to_be_focused()


def test_class_attribute(page):
    """Record primary (blue) button click and press ok in alert popup.
    Then execute your test to make sure that it can identify the button using btn-primary class."""
    page.goto("/")
    page.click('text=Class Attribute')
    primary_button = page.locator("//button[contains(concat(' ', normalize-space(@class), ' '), ' btn-primary ')]")
    primary_button.click()
    page.on('dialog', lambda dialog: dialog.accept())

    expect(primary_button).to_be_focused()


def test_hidden_layers(page):
    """Execute the test to make sure that green button can not be hit twice."""
    page.goto("/")
    page.click('text=Hidden Layers')

    expect(page.locator("id=blueButton")).not_to_be_visible()

    page.locator("id=greenButton").click()
    page.locator("id=blueButton").click()

    expect(page.locator("id=blueButton")).to_be_focused()
    expect(page.locator("id=greenButton")).not_to_be_focused()  # means it can not be clicked


def test_load_delay(page):
    """Navigate to Home page and record Load Delays link click and button click on this page.
    Then play the test. It should wait until page is loaded."""
    page.goto("/")
    page.click('text=Load Delay')

    expect(page.locator("text=Button Appearing After Delay")).to_be_visible()


def test_ajax_data(page):
    """Press the button below and wait for data to appear (15 seconds), click on text of the loaded label.
    Then execute your test to make sure it waits for label text to appear."""
    page.goto('/ajax')
    page.locator("text=Button Triggering AJAX Request").click()
    page.locator('text=Data loaded with AJAX get request.').wait_for()

    expect(page.locator('text=Data loaded with AJAX get request.')).to_be_visible()
    # expect(page.locator('.bg-success')).to_have_text('Data loaded with AJAX get request.')  # alternative assertion


def test_client_side_delay(page):
    """Press the button below and wait for data to appear (15 seconds), click on
    text of the loaded label. Then execute your test to make sure it waits for label text to appear."""
    page.goto('/clientdelay')
    page.click('.btn-primary')
    page.wait_for_selector('.bg-success', timeout=25000)  # timeout in ms (not seconds)

    expect(page.locator('.bg-success')).to_have_text('Data calculated on the client side.')


def test_click(page):
    """Record button click. The button becomes green after clicking.
    Then execute your test to make sure that it is able to click the button."""
    page.goto("/")
    page.click('text=Click')
    page.click('text=Button That Ignores DOM Click Event')
    page.click('text=Button That Ignores DOM Click Event')

    expect(page.locator('#badButton')).to_have_class('btn btn-success')
    page.click('text=Button That Ignores DOM Click Event')
    expect(page.locator('#badButton')).to_be_focused()  # means it was clicked


def test_text_input(page):
    """Record setting text into the input field and pressing the button.
    Then execute your test to make sure that the button name is changing."""
    page.goto("/")
    page.click('text=Text Input')
    page.locator('id=newButtonName').click()
    page.locator('id=newButtonName').fill('')  # this clears input field
    page.fill('id=newButtonName', 'My_Sample_Button')
    page.click('id=updatingButton')

    expect(page.locator('id=updatingButton')).to_have_text('My_Sample_Button')


def test_scrollbars(page):
    """Find a button in the scroll view and record button click.
    Update your test to automatically scroll the button into a visible area."""
    page.goto("/")
    page.click('text=Scrollbars')
    page.focus('#hidingButton')
    page.click('#hidingButton')

    expect(page.locator('#hidingButton')).to_be_focused()  # witch means it is clickable


def test_dynamic_table(page):  # NOT DONE
    """For Chrome process get value of CPU load. Compare it with value in the yellow label."""
    page.goto("/")
    page.click('text=Dynamic Table')


def test_verify_text(page):
    """Create a test that finds an element with Welcome... text."""
    page.goto("/")
    page.click('text=Verify Text')

    # expect(page.locator("//span[.='Welcome UserName!']")).to_have_text("Welcome UserName!") DOES NOT WORK ON PURPOSE
    expect(page.locator("//span[normalize-space(.)='Welcome UserName!']")).to_have_text("Welcome UserName!")


def test_progress_bar(page):  # NOT DONE
    """Create a test that clicks Start button and then waits for the progress bar to reach 75%. Then the test should
    click Stop. The less the difference between value of the stopped progress bar and 75% the better your result."""
    page.goto("/")
    page.click('text=Progress Bar')
    page.click('id=startButton')
    progress_bar = page.locator('id=progressBar')
    if progress_bar.get_attribute("aria-valuenow") == "30":
        page.click('id=stopButton')

    expect(progress_bar).to_have_attribute(name='aria-valuenow', value='30')


def test_visibility(page):
    """Determine if other buttons are visible or not"""
    page.goto("/")
    page.click('text=Visibility')
    page.click('id=hideButton')

    expect(page.locator('id=removedButton')).not_to_be_visible()
    expect(page.locator('id=zeroWidthButton')).to_be_hidden()
    expect(page.locator('id=overlappedButton')).to_be_visible()
    expect(page.locator('id=transparentButton')).to_have_attribute(name="style", value="opacity: 0;")
    expect(page.locator('id=invisibleButton')).to_have_attribute(name="style", value="visibility: hidden;")
    expect(page.locator('id=notdisplayedButton')).to_have_attribute(name="style", value="display: none;")
    expect(page.locator('id=offscreenButton')).to_be_visible()


def test_sample_app(page):
    """Fill in and submit the form. For successful login use any non-empty user name and `pwd` as password."""
    # valid login path
    page.goto("/")
    page.click('text=Sample App')
    time.sleep(1)  # In my case, login button loads first. I need to wait a sec for page to fully load
    page.locator('[name="UserName"]').fill('NonEmpty')
    page.locator('[name="Password"]').fill('pwd')
    page.click('id=login')
    expect(page.locator('id=loginstatus')).to_have_text('Welcome, NonEmpty!')
    page.click('id=login')

    # invalid login path
    page.goto("/")
    page.click('text=Sample App')
    time.sleep(1)
    page.locator('[name="UserName"]').fill('NonEmpty')
    page.locator('[name="Password"]').fill('wrong_password')
    page.click('id=login')
    expect(page.locator('id=loginstatus')).to_have_text('Invalid username/password')


def test_mouse_over(page):
    """Record 2 consecutive link clicks. Execute the test and make sure that click count is increasing by 2."""
    page.goto("/")
    page.click('text=Mouse Over')
    page.locator('text=Click me').hover()
    page.locator('text=Click me').dblclick()
    time.sleep(2)  # so we could see anything

    expect(page.locator('id=clickCount')).to_have_text('2')
    page.locator('text=Click me').dblclick()
    expect(page.locator('id=clickCount')).to_have_text('4')


def test_non_breaking_space(page):
    """Record 2 consecutive link clicks. Execute the test and make sure that click count is increasing by 2."""
    page.goto("/")
    page.click('text=Non-Breaking Space')
    # page.locator('xpath=//button[text()="My Button"]').click()  # DOES NOT WORK on purpose
    page.locator('button', has_text='My Button').click()

    expect(page.locator('button', has_text='My Button')).to_be_focused()


def test_overlapped_element(page):
    """Record setting text into the Name input field (scroll element before entering the text).
    Then execute your test to make sure that the text was entered correctly."""
    page.goto("/")
    page.click('text=Overlapped Element')
    page.locator('id=id').fill('first_text_input')
    page.locator('id=name').hover()
    page.mouse.wheel(0, 150)
    page.locator('id=name').fill('second_text_input', force=True)

    expect(page.locator('id=id')).to_have_value('first_text_input')
    expect(page.locator('id=name')).to_have_value('second_text_input')


def test_shadow_dom(page):
    """Add an assertion step to your test to compare the value from the clipboard with the value of the input field.
    Then execute the test to make sure that the assertion step is not failing."""
    page.goto("/")
    page.click('text=Shadow DOM')
    page.locator('id=buttonGenerate').click()
    page.locator('id=buttonCopy').click()  # In my case, this button does not work (empty clipboard after click)

    page.locator('id=editField').click()
    page.keyboard.press(key="Meta+A")  # for Windows use "Control+A"
    page.keyboard.press(key="Meta+C")  # for Windows use "Control+C"
    clipboard_paste = pyperclip.paste()  # pyperclip is simple module for clipboard management
    input_field_value = page.locator('id=editField')

    expect(input_field_value).to_have_value(clipboard_paste)  # for macOS only

# COMING NEXT - PAGE OBJECT PATTERN
