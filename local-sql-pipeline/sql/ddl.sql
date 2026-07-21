-- ============================================================
-- Local SQL Pipeline — DDL
-- Base de datos, esquema y tabla de precios horarios simulados
-- ============================================================

IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = 'energydb')
    CREATE DATABASE energydb;
GO

USE energydb;
GO

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'stg')
    EXEC('CREATE SCHEMA stg');
GO

IF NOT EXISTS (SELECT 1 FROM sys.tables t
               JOIN sys.schemas s ON t.schema_id = s.schema_id
               WHERE s.name = 'stg' AND t.name = 'precios_horarios')
BEGIN
    CREATE TABLE stg.precios_horarios (
        fecha_hora        DATETIME2(0)   NOT NULL,  -- Timestamp del precio (hora)
        precio_eur_mwh    DECIMAL(10,2)  NOT NULL,  -- Precio en EUR/MWh
        zona              VARCHAR(50)    NOT NULL,  -- Zona geográfica
        fecha             AS CONVERT(DATE, fecha_hora) PERSISTED,  -- Columna calculada para consultas por día
        fecha_carga       DATETIME2(0)   NOT NULL DEFAULT SYSUTCDATETIME(),  -- Auditoría de carga

        CONSTRAINT PK_precios_horarios PRIMARY KEY (fecha_hora, zona)
    );

    CREATE INDEX IX_precios_fecha ON stg.precios_horarios (fecha);
END
GO
