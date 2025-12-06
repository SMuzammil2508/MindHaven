from app import app, db, User, TherapistProfile

with app.app_context():
    # ---------------------------------------------------------
    # STEP 1: Create the User (Login Credentials)
    # ---------------------------------------------------------
    # We create a generic User, but mark their role as 'therapist'
    therapist_user = User(
        username="Dr_Sarah_Peace", 
        email="sarah@mindhaven.com",
        role="therapist"
    )
    therapist_user.set_password("securepassword123") # Hashing handled here

    # We must add and commit the user FIRST so they get an ID
    db.session.add(therapist_user)
    db.session.commit() 

    # ---------------------------------------------------------
    # STEP 2: Create the Profile (Professional Info)
    # ---------------------------------------------------------
    # Now we link this profile to the user we just created using 'therapist_user.id'
    therapist_profile = TherapistProfile(
        user_id=therapist_user.id,  # <--- THIS LINKS THEM
        specialization="Wellness Coach",
        bio="I specialize in anxiety and stress management."
    )

    db.session.add(therapist_profile)
    db.session.commit()

    print("Success! Created User 'Dr_Sarah_Peace' linked to a Therapist Profile.")