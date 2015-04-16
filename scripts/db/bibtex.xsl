<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" indent="no" encoding="UTF-8"/>

  <!-- traverse the nodes -->
  <xsl:template match="@*|node()">
    <xsl:apply-templates select="@*|node()"/>
  </xsl:template>

  <!-- output the record type and bib key -->
  <xsl:template match="/bibl/*[not(name() = 'key' or name() = 'note')]">@<xsl:value-of select="name(.)"/>{<xsl:value-of select="normalize-space(/bibl/key)"/>,
<xsl:apply-templates select="@*|node()"/>}</xsl:template>

  <!-- convert all thrid-level bibl nodes to key-value pairs -->
  <xsl:template match="/bibl/*/*">
    <xsl:text>  </xsl:text><xsl:value-of select="name(.)"/>={<xsl:value-of select="normalize-space(.)"/>},
</xsl:template> 

</xsl:stylesheet>
