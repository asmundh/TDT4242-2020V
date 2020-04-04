describe("Test that project owner should be able to accept offers", function() {
    
    const seedFileName = 'fr6_seed.json'

    before(function() {
        cy.init_db_by_seed(seedFileName)
    })

    it("Should click deliver and add a role, a member and change permissions of member.(FR6, FR7, FR10)", function() {
        cy.login("admin", "qwerty123")
        cy.contains('Costumer Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()

        cy.get('button').contains("Add Role").click()
        cy.wait(400)
        cy.get('input[name="name"]').type('Administering')
        cy.get('div[id="seeTeamModal"]').contains('Add Role').click()

        cy.wait(300)
        cy.contains('User').click()
        cy.get('div[id="seeTeamAddModal1"] select').select('harrypotter').invoke('val')
        cy.get('div[id="seeTeamAddModal1"]').contains('Add Members').click()

        cy.contains('Change permissions').click()
        cy.get('input[name="permission-upload-1"]').check()
        cy.get('div[id="seePermissionModal"]').contains('Change permissions').click()

        cy.contains('Sign out').click()
    })

    it("Should log in as project owner and give new permissions to a user (FR9)", function() {
        cy.login("joe", "qwerty123")
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.get('harrypotter').should('not.exist')
        cy.get('a[href="/projects/2/tasks/2/permissions/"]').click()
        cy.get('select[id="id_user"]').select('harrypotter').invoke('val')
        cy.get('select[id="id_permission"]').select('Modify').invoke('val')
        cy.get('button[type="submit"]').click()        
        cy.contains('harrypotter').should('exist')
    })

    it("should log into entrepreneur and deliver a file", function() {
        cy.login("admin", "qwerty123")
        cy.contains('Costumer Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.contains(/\bDeliver\b/).click()
        cy.wait(600)
        cy.get('div[id="seeDeliverModal"] textarea[name="comment"]').type('This is not it, this is just a comment')
        cy.get('input[type="file"]').attachFile('../seeds/fr5_seed.json')
        cy.get('div[id="seeDeliverModal"]').contains('Deliver').click()
        cy.wait(300)
        cy.contains('Status: Pending')
        cy.get('a[href="/projects/2/tasks/2/upload/"]').click()
        cy.get('input[type="file"]').attachFile('../seeds/fr5_seed.json')
        cy.contains('Upload File').click()
    })

    it("Should be possible for task participant to upload file if they have modify rights.(FR12)", function() {
        cy.login("harrypotter", "qwerty123")
        cy.wait
        cy.contains('Costumer Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.get('a[href="/projects/2/tasks/2/upload/"]').click()
        cy.get('input[type="file"]').attachFile('../seeds/fr6_seed.json')
        cy.contains('Upload File').click()
        cy.contains('fr6_seed.json')
    })
})