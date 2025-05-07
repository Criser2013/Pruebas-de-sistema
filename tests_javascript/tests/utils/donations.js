exports.donations = async (page, importe, empresa, nombre) => {
  await page.goto(
    "http://localhost:80/don/card.php?leftmenu=donations&action=create"
  );
  
  await page.fill('input[name="re"]', "04/05/2025");
  await page.fill('input[name="amount"]', importe);
  await page.selectOption('select[name="public"]', "0");
  await page.fill('input[name="societe"]', empresa);
  await page.fill('input[name="firstname"]', nombre);
  await page.click('input[name="save"]');
  await page.waitForURL(/\/don\/card\.php\?id=\d+/, { timeout: 5000 });

};
