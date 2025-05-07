const { test, expect } = require("@playwright/test");
const { login } = require("./utils/login.js"); // Adjust the path as necessary

// Set the locale for the test suite
test.use({
  locale: 'es-ES'
});

test.describe("", () => {
  test.beforeEach(async ({ page }) => {
    //input your login credentials here
    await test.step("Login", async () => {
      await page.goto("http://localhost:80"); // Replace with the actual URL of your application
      await login(page, "admin", "admin"); // Call the login function to perform the login action
    });
  });

  test("C24 Clase Valida - Registrar donación y verificar redirección", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');

    await page.waitForURL(/\/don\/card\.php\?id=\d+/, { timeout: 5000 });

    const currentUrl = page.url();
    expect(currentUrl).toMatch(/\/don\/card\.php\?id=\d+/);
  });

  // -----------

  test("C25 Clase Invalida - Registrar donación con importe negativo", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04/05/2025");
    await page.fill('input[name="amount"]', "-10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Importe' no puede ser negativo")).toBeVisible();
  });

  // -----------

  test("C26 Clase Invalida - Registrar donación con importe vacio", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04/05/2025");
    await page.fill('input[name="amount"]', "");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Importe' es obligatorio")).toBeVisible();
  });

  // -----------

  test("C27 Clase Invalida - Registrar donación con importe 0", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04/05/2025");
    await page.fill('input[name="amount"]', "0");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Importe' debe tener una cantidad mayor a 0")).toBeVisible();
  });

  // -----------

  test("C28 Clase Invalida - Registrar donación con el campo importe con letras", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04/05/2025");
    await page.fill('input[name="amount"]', "ABC");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Importe' es obligatorio")).toBeVisible();
  });
  
  // -----------

  test("C29 Clase valida - Registrar donación con una fecha valida", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04/05/2025");
    await page.fill('input[name="amount"]', "10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');

    await page.waitForURL(/\/don\/card\.php\?id=\d+/, { timeout: 5000 });

    const currentUrl = page.url();
    expect(currentUrl).toMatch(/\/don\/card\.php\?id=\d+/);
  });
  
  // -----------

  test("C30 Clase invalida - Registrar donación con el campo fecha en letras", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "ABC");
    await page.fill('input[name="amount"]', "10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');
    
    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Fecha' es obligatorio")).toBeVisible();
  });

  // -----------

  test("C31 Clase invalida - Registrar donación con el campo fecha en otro formato", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "2025/05/04");
    await page.fill('input[name="amount"]', "10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');
    
    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Fecha' debe ser en formato ¨DD/MM/AAAA¨")).toBeVisible();
  });

  // -----------

  test("C32 Clase invalida - Registrar donación con el campo fecha en numeros", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04052025");
    await page.fill('input[name="amount"]', "10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');
    
    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Fecha' debe ser en formato ¨DD/MM/AAAA¨")).toBeVisible();
  });
  
  // -----------

  test("C33 Clase invalida - Registrar donación con el campo fecha vacio", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "");
    await page.fill('input[name="amount"]', "10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');
    
    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Fecha' es obligatorio")).toBeVisible();
  });
  
  // -----------

  test("C34 Clase invalida - Registrar donación con el campo fecha vacio", async ({
    page,
  }) => {
    await page.goto(
      "http://localhost:80/don/card.php?leftmenu=donations&action=create"
    );

    await page.fill('input[name="re"]', "04/05/1025");
    await page.fill('input[name="amount"]', "10000");
    await page.selectOption('select[name="public"]', "0");
    await page.click('input[name="save"]');
    
    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo 'Fecha' es muy antigua/lejena")).toBeVisible();
  });
});
