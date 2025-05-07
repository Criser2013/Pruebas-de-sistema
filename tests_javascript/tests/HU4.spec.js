const { test, expect } = require("@playwright/test");
const { login } = require("./utils/login.js"); // Adjust the path as necessary
const { bankAccount } = require("./utils/bankAccount.js"); // Adjust the path as necessary

// Set the locale for the test suite
test.use({
  locale: "es-ES",
});

test.describe("", () => {
  test.beforeEach(async ({ page }) => {
    //input your login credentials here
    await test.step("Login", async () => {
      await page.goto("http://localhost:80"); // Replace with the actual URL of your application
      await login(page, "admin", "admin"); // Call the login function to perform the login action
    });
  });

  test("C35 - Crear nuevo salario sin etiqueta", async ({ page }) => {
    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "");
    await page.fill('input[name="datesp"]', "06/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.setChecked('input[name="auto_create_paiement"]', false);
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Etiqueta' es obligatorio")).toBeVisible();
  });

  test("C36 - Crear nuevo salario con fecha erronea", async ({ page }) => {
    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "Pago");
    await page.fill('input[name="datesp"]', "08/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.setChecked('input[name="auto_create_paiement"]', false);
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("Las fechas de periodo deben ser validas")).toBeVisible();
  });

  test("C37 - Crear nuevo salario con importe erroneo (negativo)", async ({ page }) => {
    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "Pago");
    await page.fill('input[name="datesp"]', "06/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "-10000");
    await page.setChecked('input[name="auto_create_paiement"]', false);
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText('El campo "Importe" deben ser validas')).toBeVisible();
  });

  test("C38 - Crear nuevo salario con todos los datos y sin grabar pago", async ({ page }) => {
    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "Pago");
    await page.fill('input[name="datesp"]', "06/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.setChecked('input[name="auto_create_paiement"]', false);
    await page.click('input[name="save"]');

    await page.waitForURL(/\/salaries\/card\.php\?id=\d+/, { timeout: 5000 });
    const currentUrl = page.url();
    expect(currentUrl).toMatch(/\/salaries\/card\.php\?id=\d+/);
  });

  test("C39 - Crear nuevo salario con todos los datos pero sin la cuenta bancaria", async ({ page }) => {
    
    await bankAccount(page); // Call the bank account function to perform the action

    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "Pago");
    await page.fill('input[name="datesp"]', "06/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.setChecked('input[name="auto_create_paiement"]', true);
    await page.click('#select2-selectpaymenttype-container');
    await page.waitForSelector('#select2-selectpaymenttype-results');
    await page.click('li.select2-results__option:has-text("Efectivo")');
    await page.fill('input[name="datep"]', "30/05/2025");
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Cuenta bancaria' es obligatorio")).toBeVisible();
  });

  test("C40 - Crear nuevo salario con todos los datos pero sin seleccionar forma de pago", async ({ page }) => {

    await bankAccount(page); // Call the bank account function to perform the action

    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "Pago");
    await page.fill('input[name="datesp"]', "06/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.setChecked('input[name="auto_create_paiement"]', true);
    await page.click('#select2-selectaccountid-container');
    await page.waitForSelector('.select2-results__option');
    await page.click('li.select2-results__option:has-text("cuenta")');
    await page.fill('input[name="datep"]', "30/05/2025");
    await page.click('input[name="save"]');

    
    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Forma de pago' es obligatorio")).toBeVisible();
  });

  test("C41 - Crear nuevo salario con todos los datos pero sin el campo fecha pago", async ({ page }) => {

    await bankAccount(page); // Call the bank account function to perform the action

    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "Pago");
    await page.fill('input[name="datesp"]', "06/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.setChecked('input[name="auto_create_paiement"]', true);
    await page.click('#select2-selectaccountid-container');
    await page.waitForSelector('.select2-results__option');
    await page.click('li.select2-results__option:has-text("cuenta")');
    await page.click('#select2-selectpaymenttype-container');
    await page.waitForSelector('#select2-selectpaymenttype-results');
    await page.click('li.select2-results__option:has-text("Efectivo")');
    await page.fill('input[name="datep"]', "");
    await page.click('input[name="save"]');

    
    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Fecha de pago' es obligatorio")).toBeVisible();
  });

  test("C42 - Crear nuevo salario con todos los datos y grabando pago", async ({ page }) => {

    await bankAccount(page); // Call the bank account function to perform the action

    await page.goto(
      "http://localhost/salaries/card.php?leftmenu=tax_salary&action=create"
    );

    await page.fill('input[name="label"]', "Pago");
    await page.fill('input[name="datesp"]', "06/05/2025");
    await page.fill('input[name="dateep"]', "07/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.setChecked('input[name="auto_create_paiement"]', true);
    await page.click('#select2-selectaccountid-container');
    await page.waitForSelector('.select2-results__option');
    await page.click('li.select2-results__option:has-text("cuenta")');
    await page.click('#select2-selectpaymenttype-container');
    await page.waitForSelector('#select2-selectpaymenttype-results');
    await page.click('li.select2-results__option:has-text("Efectivo")');
    await page.fill('input[name="datep"]', "30/05/2025");
    await page.click('input[name="save"]');

    
    await page.waitForURL(/\/salaries\/card\.php\?id=\d+/, { timeout: 5000 });
    const currentUrl = page.url();
    expect(currentUrl).toMatch(/\/salaries\/card\.php\?id=\d+/);
  });


});
