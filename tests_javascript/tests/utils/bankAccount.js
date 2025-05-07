exports.bankAccount = async (page) => {
    await page.goto(
        "http://localhost/compta/bank/card.php?action=create&leftmenu="
      );
    await page.fill('input[name="ref"]', "referencia");
    await page.fill('input[name="label"]', "cuenta");
    // Abrir el menú desplegable
    await page.click('#select2-type-container');

    // Esperar a que se carguen las opciones
    await page.waitForSelector('.select2-results__option');

    // Hacer clic en la opción deseada
    await page.click('li.select2-results__option:has-text("Cuenta caja/efectivo")');
    await page.click('input[name="save"]');
  };