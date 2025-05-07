const { test, expect } = require("@playwright/test");
const { login } = require("./utils/login.js"); // Adjust the path as necessary
const { donations } = require("./utils/donations.js"); // Adjust the path as necessary
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

  test("C86 Clase Valida - lista de donación sin filtros", async ({ page }) => {
    await page.goto("http://localhost/don/stats/index.php?leftmenu=");

    // Paso 2: Verificar que hay elementos en la tabla (sin filtro)
    const allRows = await page.locator(
      ".div-table-responsive-no-min tbody tr:nth-child(n+1)"
    ); // Obtener todas las filas de la tabla
    const rowCount = await allRows.count(); // Obtener el número de filas

    // Verificar que la tabla tiene al menos una fila (es decir, que no está vacía)
    expect(rowCount).toBeGreaterThan(0); // Asegura que haya al menos una fila visible
  });

  test("C87 Clase Valida - lista de donación con tipo de terceros valido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/stats/index.php?leftmenu=");
    const filtro = "Otro"; // Cambia esto al valor que deseas filtrar
    await page.click("#select2-typent_id-container");
    await page.waitForSelector("#select2-typent_id-results");
    await page.click(`li.select2-results__option:has-text("${filtro}")`);
    await page.click('input[name="submit"]'); // Hacer clic en el botón de búsqueda

    await page.waitForSelector(".div-table-responsive tbody tr", {
      timeout: 5000,
    }); // Esperar a que aparezcan las filas
    const allRows = await page.locator(
      ".div-table-responsive-no-min tbody tr:nth-child(n+1)"
    );
    const rowCount = await allRows.count(); // Obtener el número de filas

    expect(rowCount).toBeGreaterThan(0);
  });

  test("C88 Clase Invalida - lista de donación con tipo de terceros invalido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/stats/index.php?leftmenu=");

    const filtro = "Inexistente"; // Cambia esto al valor que deseas filtrar
    await page.click("#select2-typent_id-container");
    await page.waitForSelector("#select2-typent_id-results");
    const optionExists = await page
      .locator("#select2-search_status-results li")
      .locator("text=" + filtro)
      .count();

    expect(optionExists).toBe(0); // Si la opción no existe, el contador debe ser 0
    // Hacer clic en un área aleatoria para quitar el foco
    await page.click("body");
  });

  test("C89 Clase Valida - lista de donación con estado valido", async ({
    page,
  }) => {
    await donations(page, "10000", "empresa", "nombre"); // Llama a la función donations para crear donaciones de prueba

    await page.goto("http://localhost/don/stats/index.php?leftmenu=");

    const filtro = "Promesa no validada"; // Cambia esto al valor que deseas filtrar
    await page.click("#select2-status-container");
    await page.waitForSelector("#select2-status-results");
    await page.click(`li.select2-results__option:has-text("${filtro}")`);
    await page.click('input[name="submit"]'); // Hacer clic en el botón de búsqueda

    const allRows = await page.locator(
      ".div-table-responsive-no-min tbody tr:nth-child(n+1)"
    );
    const rowCount = await allRows.count(); // Obtener el número de filas

    expect(rowCount).toBeGreaterThan(0); // Verifica que haya al menos una fila visible
  });

  test("C90 Clase Invalida - lista de donación con estado invalido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/stats/index.php?leftmenu=");

    const filtro = "Inexistente"; // Cambia esto al valor que deseas filtrar
    await page.click("#select2-status-container");
    await page.waitForSelector("#select2-status-results");
    const optionExists = await page
      .locator("#select2-search_status-results li")
      .locator("text=" + filtro)
      .count();

    expect(optionExists).toBe(0); // Si la opción no existe, el contador debe ser 0
    // Hacer clic en un área aleatoria para quitar el foco
    await page.click("body");
  });

  test("C91 Clase Valida - lista de donación con año valido", async ({
    page,
  }) => {
    await donations(page, "10000", "empresa", "nombre"); // Llama a la función donations para crear donaciones de prueba
    await page.goto("http://localhost/don/stats/index.php?leftmenu=");

    const filtro = "2025"; // Cambia esto al valor que deseas filtrar
    await page.click("#select2-year-container");
    await page.waitForSelector("#select2-year-results");
    await page.click(`li.select2-results__option:has-text("${filtro}")`);
    await page.click('input[name="submit"]'); // Hacer clic en el botón de búsqueda
    
    const rows = await page.locator(".div-table-responsive-no-min tbody tr:nth-child(n+1)"); // Obtener todas las filas de la tabla
    const allRows = await rows.locator('td:nth-child(1)').allTextContents();
    // Asegúrate de que todos los elementos coincidan con el filtro
    const allMatch = allRows.every(amount => amount === filtro); 

    expect(allMatch).toBe(true); // Verifica que todos los elementos coincidan con el filtro
  });

  test("C92 Clase Invalida - lista de donación con año invalido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/stats/index.php?leftmenu=");

    const filtro = "1030"; // Cambia esto al valor que deseas filtrar
    await page.click("#select2-year-container");
    await page.waitForSelector("#select2-year-results");
    const optionExists = await page
      .locator("#select2-search_status-results li")
      .locator("text=" + filtro)
      .count();

    expect(optionExists).toBe(0); // Si la opción no existe, el contador debe ser 0
    // Hacer clic en un área aleatoria para quitar el foco
    await page.click("body");
  });
});
