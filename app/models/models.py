from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


# ─────────────────────────────────────────────
# Tables principales
# ─────────────────────────────────────────────

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id_utilisateur  = Column(Integer, primary_key=True, autoincrement=True)
    nom             = Column(String(100), nullable=False)
    prenom          = Column(String(100), nullable=False)
    email           = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)

    # Relations
    inscriptions   = relationship("Sinscrire",    back_populates="utilisateur")
    recommandations= relationship("Recommander",  back_populates="utilisateur")
    passages       = relationship("Passer",       back_populates="utilisateur")
    obtenus        = relationship("Obtenir",      back_populates="utilisateur")


class Formation(Base):
    __tablename__ = "formations"

    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    titre        = Column(String, nullable=False)
    description  = Column(String, nullable=True)
    duree        = Column(String, nullable=True)

    # Relations
    sessions     = relationship("SessionFormation", back_populates="formation")
    modules      = relationship("Posseder",         back_populates="formation")
    suggestions  = relationship("Suggerer",         back_populates="formation")


class ModuleFormation(Base):
    __tablename__ = "modules_formations"

    id_module = Column(Integer, primary_key=True, autoincrement=True)
    titre     = Column(String, nullable=False)
    contenu   = Column(String, nullable=False)
    duree     = Column(String, nullable=True)

    # Relations
    formations = relationship("Posseder",  back_populates="module")
    resultats  = relationship("Resultat",  back_populates="module")


class SessionFormation(Base):
    __tablename__ = "sessions_formations"

    id_session  = Column(Integer, primary_key=True, autoincrement=True)
    id_formation= Column(Integer, ForeignKey("formations.id_formation"), nullable=False)
    date_debut  = Column(String, nullable=True)
    date_fin    = Column(String, nullable=True)
    lieu        = Column(String, nullable=True)
    capacite    = Column(Integer, nullable=True)
    mode        = Column(Boolean, nullable=True)  # présentiel/non

    # Relations
    formation    = relationship("Formation",  back_populates="sessions")
    inscriptions = relationship("Sinscrire",  back_populates="session")


class RecommandationIA(Base):
    __tablename__ = "recommandations_ia"

    id_recommandation = Column(Integer, primary_key=True, autoincrement=True)
    date              = Column(String, nullable=True)
    score_pertinence  = Column(Integer, nullable=False)
    motif             = Column(String, nullable=True)

    # Relations
    suggestions   = relationship("Suggerer",    back_populates="recommandation")
    recommandeurs = relationship("Recommander", back_populates="recommandation")


class Resultat(Base):
    __tablename__ = "resultats"

    id_resultats  = Column(Integer, primary_key=True, autoincrement=True)
    id_module     = Column(Integer, ForeignKey("modules_formations.id_module"), nullable=False)
    note          = Column(Integer, nullable=True)
    reussite      = Column(Boolean, nullable=True)
    date_passage  = Column(String, nullable=False)
    tentative     = Column(Boolean, nullable=True)

    # Relations
    module   = relationship("ModuleFormation", back_populates="resultats")
    passages = relationship("Passer",          back_populates="resultat")
    obtenus  = relationship("Obtenir",         back_populates="resultat")


# ─────────────────────────────────────────────
# Tables de liaison (many-to-many)
# ─────────────────────────────────────────────

class Posseder(Base):
    """Association Formation <-> Module"""
    __tablename__ = "posseder"

    id_module    = Column(Integer, ForeignKey("modules_formations.id_module"), primary_key=True)
    id_formation = Column(Integer, ForeignKey("formations.id_formation"),      primary_key=True)

    module    = relationship("ModuleFormation", back_populates="formations")
    formation = relationship("Formation",       back_populates="modules")


class Suggerer(Base):
    """Association Recommandation <-> Formation"""
    __tablename__ = "suggerer"

    id_recommandation = Column(Integer, ForeignKey("recommandations_ia.id_recommandation"), primary_key=True)
    id_formation      = Column(Integer, ForeignKey("formations.id_formation"),              primary_key=True)

    recommandation = relationship("RecommandationIA", back_populates="suggestions")
    formation      = relationship("Formation",        back_populates="suggestions")


class Sinscrire(Base):
    """Association Utilisateur <-> Session"""
    __tablename__ = "sinscrire"

    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), primary_key=True)
    id_session     = Column(Integer, ForeignKey("sessions_formations.id_session"), primary_key=True)
    date_inscription = Column(String, nullable=False)

    utilisateur = relationship("Utilisateur",     back_populates="inscriptions")
    session     = relationship("SessionFormation", back_populates="inscriptions")


class Recommander(Base):
    """Association Utilisateur <-> Recommandation"""
    __tablename__ = "recommander"

    id_utilisateur    = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"),          primary_key=True)
    id_recommandation = Column(Integer, ForeignKey("recommandations_ia.id_recommandation"), primary_key=True)

    utilisateur    = relationship("Utilisateur",      back_populates="recommandations")
    recommandation = relationship("RecommandationIA", back_populates="recommandeurs")


class Passer(Base):
    """Association Utilisateur <-> Resultat"""
    __tablename__ = "passer"

    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), primary_key=True)
    id_resultats   = Column(Integer, ForeignKey("resultats.id_resultats"),      primary_key=True)

    utilisateur = relationship("Utilisateur", back_populates="passages")
    resultat    = relationship("Resultat",    back_populates="passages")


class Obtenir(Base):
    """Association Utilisateur <-> Resultat (obtention)"""
    __tablename__ = "obtenir"

    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), primary_key=True)
    id_resultats   = Column(Integer, ForeignKey("resultats.id_resultats"),      primary_key=True)

    utilisateur = relationship("Utilisateur", back_populates="obtenus")
    resultat    = relationship("Resultat",    back_populates="obtenus")