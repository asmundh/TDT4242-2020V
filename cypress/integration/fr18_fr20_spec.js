describe("Lists all projects in corect categories(FR18 and FR20)", function() {
    const seedFileName = 'fr18_seed.json'
    
    before(function() {
        cy.init_db_by_seed(seedFileName)
    })

    it('Should list two projects for each category(FR18 and FR20)', function() {
        cy.login('admin', 'qwerty123')
        cy.get('a[href="/projects/"]').click()

        cy.get('div[id="Cleaning"]').find('div[class="row projects-view"]').children().should('have.length', 2)
        cy.wait(400)


        cy.get('a[id="category-Painting"]').click()
        cy.get('div[id="Painting"]').find('div[class="row projects-view"]').children().should('have.length', 2)
        cy.wait(400)

        cy.get('a[id="category-Gardening"]').click()
        cy.get('div[id="Gardening"]').find('div[class="row projects-view"]').children().should('have.length', 3)

    })
})
