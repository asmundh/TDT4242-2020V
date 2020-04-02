// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//

Cypress.Commands.add("login", (username, password) => {
    cy.visit('http://localhost:8000/')
    cy.contains('Sign in').click()

    cy.get('input[name="username"]').type(username)
    cy.get('input[name="password"]').type(password)
    cy.get('button[type=submit]').click()
    })

Cypress.Commands.add("reset_db_only_categories", () => {
    cy.exec('python manage.py flush --no-input')
    cy.exec('python manage.py loaddata test_seed_categories.json')
    })

Cypress.Commands.add("init_test_db", () => {
    cy.exec('rm -r db.sqlite3')
    cy.exec('python manage.py migrate')
    cy.exec('python manage.py loaddata test_seed_full_db.json')
 })

 Cypress.Commands.add("init_db_by_seed", (seedFileName) => {
    cy.exec('rm -r db.sqlite3')
    cy.exec('python manage.py migrate')
    cy.exec(`python manage.py loaddata cypress/seeds/${seedFileName}`)
 })

