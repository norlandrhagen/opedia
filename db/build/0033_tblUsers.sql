USE [Opedia]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tblUsers](
	[UserID] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nchar](50) NOT NULL,
	[FirstName] [nvarchar](500) NOT NULL,
	[FamilyName] [nvarchar](500) NOT NULL,
	[Username] [nvarchar](50) NOT NULL,
	[Password] [nvarchar](500) NOT NULL,
	[Email] [nvarchar](500) NOT NULL,
	[Institute] [nchar](500) NULL,
	[Department] [nvarchar](500) NULL,
	[Address] [nvarchar](1000) NULL,
	[City] [nvarchar](500) NULL,
	[State] [nchar](50) NULL,
	[ZipCode] [nvarchar](50) NULL,
	[Country] [nvarchar](500) NULL,
	[Telephone] [nchar](100) NULL,
	[Purpose] [nchar](1000) NULL,
	[Domain] [nchar](1000) NULL,
	[Date] [datetime] NOT NULL,
	[IP] [nchar](50) NULL,
	[IPinfo] [nchar](1000) NULL,
 CONSTRAINT [PK_tblUsers] PRIMARY KEY CLUSTERED 
(
	[UserID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[tblUsers] ADD  CONSTRAINT [DF_tblUsers_Date]  DEFAULT (getdate()) FOR [Date]
GO





SET ANSI_PADDING ON
GO

CREATE UNIQUE NONCLUSTERED INDEX [idxEmail] ON [dbo].[tblUsers]
(
	[Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO






SET ANSI_PADDING ON
GO

CREATE UNIQUE NONCLUSTERED INDEX [idxUsername] ON [dbo].[tblUsers]
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO


