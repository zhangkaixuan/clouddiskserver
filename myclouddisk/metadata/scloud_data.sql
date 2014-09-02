
/*database scloud*/

DROP TABLE IF EXISTS `data`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `data` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `m_content_type` varchar(255)  NOT NULL,
  `m_parent_id` int(10) unsigned NOT NULL default 0,
  `m_name` varchar(255) NOT NULL default '',
  `m_storage_name` varchar(255) NOT NULL default '',
  `m_tenant_name` varchar(255) NOT NULL default '',
  `m_status` varchar(255) NOT NULL default '',
  `m_url` varchar(255) NOT NULL default '',
  `m_hash` varchar(255) NOT NULL default '',
  `m_size` varchar(255) NOT NULL default '',
  `version` int(10) unsigned NOT NULL default 1,
  `created` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `useroprs`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `useroprs` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `m_opr_type` varchar(255)  NOT NULL,
  `m_content_type` varchar(255)  NOT NULL,
  `m_storage_name` varchar(255) NOT NULL default '',
  `m_user` varchar(255) NOT NULL default '',
  `m_tenant_name` varchar(255) NOT NULL default '',
  `m_parent_name` varchar(255) NOT NULL default '',
  `m_unique_url` varchar(255) NOT NULL default '',
  `m_description` varchar(255) NOT NULL default '',
  `created` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `datashare`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `datashare` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `m_content_type` varchar(255)  NOT NULL,
  `m_user_from` varchar(255) NOT NULL default '',
  `m_hash_key` varchar(255) NOT NULL default '',
  `m_name` varchar(255) NOT NULL default '',
  `m_storage_name` varchar(255) NOT NULL default '',
  `m_parent_id` int(10) unsigned NOT NULL default 0,
  `m_tenant_name` varchar(255) NOT NULL default '',
  `m_user_to` varchar(255) NOT NULL default '',
  `m_unique_url` varchar(255) NOT NULL default '',
  `m_password` varchar(255) NOT NULL default '',
  `created` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;