/**
 * Task 4 - Selenium WebDriver (JavaScript) tests for CampusConnect
 *
 * Automated cases from Task 1 (black-box):
 *   TC-DT-01  Login with correct credentials          (positive)
 *   TC-DT-02  Login with wrong password               (negative)
 *   TC-ST-01  Add a valid student, see it on the list (positive)
 *   TC-EP-02  Add a student with age 15 -> rejected   (negative)
 *
 * Run (app must already be running on http://127.0.0.1:5000):
 *   node testing/selenium/campusconnect.selenium.js
 * Options:  HEADLESS=1  run without a visible browser
 *           BASE_URL=... use a different address
 */
const { Builder, By, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:5000';
const WAIT = 10000; // explicit wait timeout (ms)
const SHOT_DIR = path.join(__dirname, 'screenshots');
const LOG_FILE = path.join(__dirname, 'selenium_results.log');

fs.mkdirSync(SHOT_DIR, { recursive: true });
fs.writeFileSync(LOG_FILE, '');

function log(message) {
  const line = `[${new Date().toISOString()}] ${message}`;
  console.log(line);
  fs.appendFileSync(LOG_FILE, line + '\n');
}

async function screenshot(driver, name) {
  const image = await driver.takeScreenshot();
  fs.writeFileSync(path.join(SHOT_DIR, `${name}.png`), image, 'base64');
}

// Unique test data for every run, so tests never clash with old records.
const stamp = Date.now();
const user = { name: 'Selenium Tester', email: `selenium.${stamp}@example.com`, password: 'Test@12345' };
const student = { name: 'Selenium Student', email: `student.${stamp}@example.com`, age: '21', marks: '85', department: 'Software Engineering' };

// ---------- reusable page actions ----------
async function register(driver, u) {
  await driver.get(`${BASE_URL}/register`);
  await driver.findElement(By.id('name')).sendKeys(u.name);
  await driver.findElement(By.id('email')).sendKeys(u.email);
  await driver.findElement(By.id('password')).sendKeys(u.password);
  await driver.findElement(By.css('form button[type="submit"]')).click();
  await driver.wait(until.urlContains('/login'), WAIT);
}

async function login(driver, email, password) {
  await driver.get(`${BASE_URL}/login`);
  await driver.findElement(By.id('email')).sendKeys(email);
  await driver.findElement(By.id('password')).sendKeys(password);
  await driver.findElement(By.css('form button[type="submit"]')).click();
}

async function flashText(driver) {
  const flash = await driver.wait(until.elementLocated(By.css('.flash')), WAIT);
  return flash.getText();
}

async function fillStudentForm(driver, s) {
  await driver.get(`${BASE_URL}/students/add`);
  await driver.wait(until.elementLocated(By.id('name')), WAIT);
  await driver.findElement(By.id('name')).sendKeys(s.name);
  await driver.findElement(By.id('email')).sendKeys(s.email);
  await driver.findElement(By.id('age')).sendKeys(s.age);
  await driver.findElement(By.css(`#department option[value="${s.department}"]`)).click();
  await driver.findElement(By.id('marks')).sendKeys(s.marks);
  await driver.findElement(By.css('form button[type="submit"]')).click();
}

// ---------- test cases ----------
async function tcDT01(driver) {
  await login(driver, user.email, user.password);
  await driver.wait(until.urlContains('/dashboard'), WAIT);
  assert.ok((await flashText(driver)).includes('Welcome back!'), 'welcome message missing');
  const heading = await driver.findElement(By.css('h1')).getText();
  assert.strictEqual(heading, 'Student dashboard');
}

async function tcDT02(driver) {
  await login(driver, user.email, 'WrongPassword!1');
  const msg = await flashText(driver);
  assert.ok(msg.includes('Invalid email or password.'), `unexpected message: ${msg}`);
  assert.ok((await driver.getCurrentUrl()).includes('/login'), 'should stay on login page');
}

async function tcST01(driver) {
  await login(driver, user.email, user.password);
  await driver.wait(until.urlContains('/dashboard'), WAIT);
  await fillStudentForm(driver, student);
  await driver.wait(until.urlContains('/dashboard'), WAIT);
  assert.ok((await flashText(driver)).includes('Student added successfully.'), 'success message missing');
  const row = await driver.wait(
    until.elementLocated(By.xpath(`//td//small[contains(text(),"${student.email}")]`)), WAIT);
  assert.ok(await row.isDisplayed(), 'new student not shown in the table');
}

async function tcEP02(driver) {
  await login(driver, user.email, user.password);
  await driver.wait(until.urlContains('/dashboard'), WAIT);
  const bad = { ...student, email: `underage.${stamp}@example.com`, age: '15' };
  await fillStudentForm(driver, bad);
  // The browser blocks the submit (min=16), so the form must stay on screen.
  await driver.wait(async () =>
    (await driver.executeScript("return document.getElementById('age').validity.rangeUnderflow")) === true, WAIT);
  assert.ok((await driver.getCurrentUrl()).endsWith('/students/add'), 'form should not be submitted');
  const validation = await driver.executeScript("return document.getElementById('age').validationMessage");
  log(`    browser validation message: "${validation}"`);
  assert.ok(validation.length > 0, 'no validation message shown');
  // Confirm that nothing was saved.
  await driver.get(`${BASE_URL}/dashboard?q=${encodeURIComponent(bad.email)}`);
  const empty = await driver.wait(until.elementLocated(By.css('td.empty')), WAIT);
  assert.ok((await empty.getText()).includes('No students found'), 'underage student was saved');
}

const tests = [
  { id: 'TC-DT-01', title: 'Login with valid credentials (positive)', fn: tcDT01 },
  { id: 'TC-DT-02', title: 'Login with wrong password (negative)', fn: tcDT02 },
  { id: 'TC-ST-01', title: 'Add valid student and find it on dashboard (positive)', fn: tcST01 },
  { id: 'TC-EP-02', title: 'Add student with age 15 is rejected (negative)', fn: tcEP02 },
];

(async function main() {
  const options = new chrome.Options().addArguments('--window-size=1280,900');
  if (process.env.HEADLESS === '1') options.addArguments('--headless=new');
  const driver = await new Builder().forBrowser('chrome').setChromeOptions(options).build();
  let passed = 0;
  let failed = 0;
  try {
    log(`Selenium run started against ${BASE_URL}`);
    await register(driver, user);
    log(`Setup: registered test user ${user.email}`);

    for (const t of tests) {
      await driver.manage().deleteAllCookies(); // every test starts logged out
      try {
        await t.fn(driver);
        await screenshot(driver, `${t.id}_PASS`);
        passed++;
        log(`PASS  ${t.id}  ${t.title}`);
      } catch (err) {
        await screenshot(driver, `${t.id}_FAIL`);
        failed++;
        log(`FAIL  ${t.id}  ${t.title}  -> ${err.message}`);
      }
    }
  } catch (err) {
    failed++;
    log(`ERROR during setup: ${err.message}`);
  } finally {
    log(`Summary: ${passed} passed, ${failed} failed, ${tests.length} total`);
    await driver.quit();
    process.exitCode = failed ? 1 : 0;
  }
})();
