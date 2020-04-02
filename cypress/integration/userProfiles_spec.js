describe("Test suite to check correct behaviour related to user descriptions", function() {

    before(function() {
        cy.exec('rm -r db.sqlite3')
        cy.exec('python manage.py migrate')
        cy.exec('python manage.py loaddata test_seed_full_db.json')
    })

    it("Should give a banner notifying of no description if no description has been set on user", function() {
        cy.visit('http://localhost:8000/user/login/')
        cy.get('input[name="username"]').type('admin')
        cy.get('input[name="password"]').type('qwerty123')        
        cy.get('button[type="submit"]').click()

        cy.contains('Your account has no description!')

        cy.get('a[href="/user/admin/"]').click()

        cy.get('input[name="description"]').clear()
        cy.get('input[name="description"]').type('Dette er så mye som en test-description. kult, hva?')
        cy.get('input[value="Edit description"]').click()
        cy.contains('Your account has been updated. ')

        cy.reload()
        cy.get('input[name="description"]').should('have.value', 'Dette er så mye som en test-description. kult, hva?')
    })

})