exports.login = async (page, username, password) => {
    await page.goto("http://localhost:80/index.php");
    await page.fill('input[id="username"]', username);
    await page.fill('input[id="password"]', password);
    await page.getByRole('button').click();
    await page.waitForURL('**/index.php?mainmenu=home');
  };