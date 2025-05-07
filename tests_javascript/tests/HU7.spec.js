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

  test("C74 Clase Valida - lista de donación sin filtros", async ({ page }) => {
    await donations(page, "10000", "empresa", "nombre"); // Llama a la función para crear una donación
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Verificar que hay elementos en la tabla (sin filtro)
    const allRows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Obtener todas las filas de la tabla
    const rowCount = await allRows.count(); // Obtener el número de filas

    // Verificar que la tabla tiene al menos una fila (es decir, que no está vacía)
    expect(rowCount).toBeGreaterThan(0); // Asegura que haya al menos una fila visible
  });

  test("C75 Clase Valida - lista de donación con filtro en referencia valido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "1";
    await page.fill('input[name="search_ref"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    // Paso 3: Esperar a que los resultados se filtren
    await page.waitForSelector(".div-table-responsive tbody tr"); // Esperar a que aparezcan las filas

    // Paso 4: Verificar que los resultados son los esperados
    const rows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Encuentra todas las filas de la tabla
    const filteredRefs = await rows.locator('td:nth-child(2)').allTextContents(); // Obtén el texto de todas las filas
    // Asegúrate de que todos los elementos coincidan con el filtro
    const allMatch = filteredRefs.every(amount => amount === filtro)

    // Verificar que todos los importes sean los esperados
    expect(allMatch).toBe(true);
  });

  test("C76 Clase Invalida - lista de donación con filtro en referencia invalido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "0";
    await page.fill('input[name="search_ref"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    // Paso 3: Esperar a que los resultados se filtren
    await page.waitForSelector(".div-table-responsive tbody tr"); // Esperar a que aparezcan las filas

    const allRows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Obtener todas las filas de la tabla
    const rowCount = await allRows.count(); // Obtener el número de filas

    // Verificar que la tabla tiene al menos una fila (es decir, que no está vacía)
    expect(rowCount).toBe(0); // Asegura que no haya ninguna fila visible

  });

  test("C77 Clase Valida - lista de donación con filtro en empresa valido", async ({
    page,
  }) => {
    await donations(page, "10000", "empresa existente", "nombre"); // Llama a la función para crear una donación
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "empresa existente";
    await page.fill('input[name="search_company"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    // Paso 3: Esperar a que los resultados se filtren
    await page.waitForSelector(".div-table-responsive tbody tr"); // Esperar a que aparezcan las filas

    // Paso 4: Verificar que los resultados son los esperados
    const rows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Encuentra todas las filas de la tabla
    const filteredRefs = await rows.locator('td:nth-child(3)').allTextContents(); // Obtén el texto de todas las filas
    // Asegúrate de que todos los elementos coincidan con el filtro
    const allMatch = filteredRefs.every(amount => amount === filtro);

    // Verificar que todos los importes sean los esperados
    expect(allMatch).toBe(true);
  });

  test("C78 Clase Invalida - lista de donación con filtro en empresa invalido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "empresa inexistente";
    await page.fill('input[name="search_company"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    // Paso 3: Esperar a que los resultados se filtren
    await page.waitForSelector(".div-table-responsive tbody tr"); // Esperar a que aparezcan las filas

    // Paso 4: Verificar que los resultados son los esperados
    const rows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Encuentra todas las filas de la tabla
    const rowCount = await rows.count(); // Obtener el número de filas

    expect(rowCount).toBe(0); // Verifica que no hay filas si el filtro no coincide
    
  });

  test("C79 Clase Valida - lista de donación con filtro en nombre valido", async ({
    page,
  }) => {
    await donations(page, "10000", "empresa", "nombre existente"); // Llama a la función para crear una donación
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "nombre existente";
    await page.fill('input[name="search_name"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    // Paso 3: Esperar a que los resultados se filtren
    await page.waitForSelector(".div-table-responsive tbody tr"); // Esperar a que aparezcan las filas

    // Paso 4: Verificar que los resultados son los esperados
    const rows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Encuentra todas las filas de la tabla
    const filteredRefs = await rows.locator('td:nth-child(4)').allTextContents(); // Obtén el texto de todas las filas
    // Asegúrate de que todos los elementos coincidan con el filtro
    const allMatch = filteredRefs.every(amount => amount === filtro);

    // Verificar que todos los importes sean los esperados
    expect(allMatch).toBe(true);
  });

  test("C80 Clase Invalida - lista de donación con filtro en nombre invalido", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "nombre inexistente";
    await page.fill('input[name="search_name"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    // Paso 3: Esperar a que los resultados se filtren
    await page.waitForSelector(".div-table-responsive tbody tr"); // Esperar a que aparezcan las filas

    // Paso 4: Verificar que los resultados son los esperados
    const rows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Encuentra todas las filas de la tabla
    const rowCount = await rows.count(); // Obtén el texto de todas las filas

    expect(rowCount).toBe(0); // Verifica que no hay filas si el filtro no coincide
  });

  test("C81 Clase Valida - lista de donación con filtro en importe valido", async ({
    page,
  }) => {
    await donations(page, "10000", "empresa", "nombre"); // Llama a la función para crear una donación
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "10000";
    await page.fill('input[name="search_amount"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    // Paso 3: Esperar a que los resultados se filtren
    await page.waitForSelector(".div-table-responsive tbody tr"); // Esperar a que aparezcan las filas

    // Paso 4: Verificar que los resultados son los esperados
    const rows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Encuentra todas las filas de la tabla
    let filteredRefs = await rows.locator('td:nth-child(6)').allTextContents(); // Obtén el texto de todas las filas
    filteredRefs = filteredRefs.map(ref => ref.replace(/,00$/, "").replace(/\./g, "")); // Elimina los últimos ",00" y todos los puntos de cada elemento
    // Asegúrate de que todos los elementos coincidan con el filtro
    const allMatch = filteredRefs.every(amount => amount === filtro); 

    // Verificar que todos los importes sean los esperados
    expect(allMatch).toBe(true);
  });

  test("C82 Clase Invalida - lista de donación con filtro en importe igual a 0", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "0";
    await page.fill('input[name="search_amount"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText("El campo ¨Importe¨ no puede ser 0")).toBeVisible();

  });

  test("C83 Clase Invalida - lista de donación con filtro en importe con numero negativo", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "-10000";
    await page.fill('input[name="search_amount"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText('El campo "Importe" no puede ser negativo')).toBeVisible();
  });

  test("C84 Clase Invalida - lista de donación con filtro en importe con cadenas de caracteres", async ({
    page,
  }) => {
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    // Paso 2: Ingresar el valor en el campo de filtro (como '35' para filtrar la columna "Ref.");
    const filtro = "ABC";
    await page.fill('input[name="search_amount"]', filtro); // Cambia el selector si es necesario
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    await page.waitForTimeout(2000); // Wait for 2 seconds to allow any error message to appear
    await expect(page.getByText('El campo "Importe" no puede contener caracteres')).toBeVisible();
  });

  test("C85 Clase Valida - lista de donación con filtro en estado", async ({
    page,
  }) => {
    await donations(page, "10000", "empresa", "nombre"); // Llama a la función para crear una donación
    await page.goto("http://localhost/don/list.php?leftmenu=donations");

    const filtro = "Promesa no validada"; // Cambia esto al valor que deseas filtrar
    const word = "No validada"
    await page.click('#select2-search_status-container');
    await page.waitForSelector('#select2-search_status-results');
    await page.click(`li.select2-results__option:has-text("${filtro}")`);
    await page.click('button[name="button_search_x"]'); // Hacer clic en el botón de búsqueda

    const rows = await page.locator(".div-table-responsive tbody tr:nth-child(n+3)"); // Obtener todas las filas de la tabla
    const allRows = await rows.locator('td:nth-child(7)').allTextContents();
    // Asegúrate de que todos los elementos coincidan con el filtro
    const allMatch = allRows.every(amount => amount === word); 

    // Verificar que todos los importes sean los esperados
    expect(allMatch).toBe(true);
  });
});
